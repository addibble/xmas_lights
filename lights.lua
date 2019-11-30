-- the main light driver
-- starts timers for ws2811 write, star pattern, and string pattern
-- updates global variables which are written in write

ws2812.init()
star_len = 241
string_len = 250

star_buf = string.rep('\0\0\0', star_len)
string_buf = string.rep('\0\0\0', string_len)

if star_tmr == nil then
    star_tmr = tmr.create()
else
    star_tmr:stop()
    print("stopping star_tmr")
end
if string_tmr == nil then
    string_tmr = tmr.create()
else
    string_tmr:stop()
    print("stopping string_tmr")
end
if ws2812_write_tmr == nil then
    ws2812_write_tmr = tmr.create()
else
    print("stopping write_tmr")
    ws2812_write_tmr:stop()
end

star_idx = 0

local star_program = function()
    if star_idx >= select(2, LFS.earth3()) then
        star_idx = 0
    end
    star_idx = star_idx + 1
    return select(1, LFS.earth3())[star_idx - 1]
end

local string_program = function()
    local ret = {}
    for i=1,string_len * 3 do
        ret[i] = string.char(math.random(1,50))
    end
    return table.concat(ret)
end

ws2812_write_tmr:register(100, tmr.ALARM_AUTO, function()
    tmr.wdclr()
    ws2812.write(string_buf .. star_buf)
end)

string_tmr:register(400, tmr.ALARM_AUTO, function()
    string_buf = string_program()
end)

star_tmr:register(2000, tmr.ALARM_AUTO, function()
    star_buf = star_program()
end)

star_tmr:start()
string_tmr:start()
ws2812_write_tmr:start()
