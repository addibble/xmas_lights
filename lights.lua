ws2812.init()
star_len = 241
string_len = 350

star_buf = ws2812.newBuffer(star_len, 3)
string_buf = ws2812.newBuffer(string_len, 3)
star_buf:fill(0,0,0)
string_buf:fill(0,0,0)

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
if program_tmr == nil then
    program_tmr = tmr.create()
else
    print("stopping program_tmr")
    program_tmr:stop()
end

local function star_program_earth3()
    star_tmr:interval(500)
    local star_idx = 0
    return function()
        if star_idx >= select(2, LFS.earth3()) then
            star_idx = 0
        end
        star_idx = star_idx + 1
        star_buf:replace(select(1, LFS.earth3())[star_idx - 1])
    end
end

local function star_program_eye()
    star_tmr:interval(3000)
    local star_idx = 0
    return function()
        if star_idx >= select(2, LFS.eye()) then
            star_idx = 0
        end
        star_idx = star_idx + 1
        star_buf:replace(select(1, LFS.eye())[star_idx - 1])
    end
end

local function string_program_random()
    string_tmr:interval(1000)
    return function()
        for i=1,string_len do
            string_buf:set(i, math.random(1,50), math.random(1,50), math.random(1,50))
        end
    end
end

local function string_program_rainbow()
    for i=1,string_len do
        string_buf:set(i, color_utils.colorWheel(i))
    end
    string_tmr:interval(100)
    return function()
        string_buf:shift(1, ws2812.SHIFT_CIRCULAR)
    end
end

local function change_program()
    rand = node.random(1,2)
    if rand == 1 then
        star_program = star_program_eye()
        string_program = string_program_random()
    else
        star_program = star_program_earth3()
        string_program = string_program_rainbow()
    end
end

change_program()

ws2812_write_tmr:register(100, tmr.ALARM_AUTO, function()
    tmr.wdclr()
    ws2812.write(string_buf .. star_buf)
end)

star_tmr:register(1000, tmr.ALARM_AUTO, function()
    star_program()
end)

string_tmr:register(1000, tmr.ALARM_AUTO, function()
    string_program()
end)

program_tmr:register(20000, tmr.ALARM_AUTO, function()
    change_program()
end)

star_tmr:start()
string_tmr:start()
ws2812_write_tmr:start()
program_tmr:start()
