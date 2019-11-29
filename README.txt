Drew's Christmas Lights
Written for a NodeMCU microcontroller and WS2812 light strings/rings
Convert animated GIFs to NodeMCU Lua to display on concentric LED rings

My setup is 5 strands of 50 lights, and a "star" of 8 concentric rings

Software included

1. Preprocessing (Linux host)
Set up and activate a python 3.8 venv in the "preprocess" dir,
install the requirements, then run the gif_to_light_pattern.py
to convert an animated gif to Lua code containing the sequences
to write to the WS2812s to play the animation, which can be
written to LFS flash on the NodeMCU.

2. Build LFS Image
Once you have a lua output from the preprocessing script, build a
LFS image to upload to the NodeMCU containing your sequence code.
Place the output lua in the nodemcu_lfs dir and name it as the
function you want to call to get it (for example, earth.lua would
be loaded like: "data = LFS.earth()"

get the firmware and tooling at https://github.com/nodemcu/nodemcu-firmware
and naviagte to app/lua/luac_cross and make in that directory to build
the luac.cross binary in the root nodemcu-firmware directory. Use that
binary in the nodemcu_lfs dir to create a lfs.img file like so:
$ luac.cross -f -o lfs.img *.lua

3. NodeMCU
First build a NodeMCU firmware with these modules: color_utils file gpio mdns net node tmr uart wifi ws2812 ws2812_effects
and max lfs size (128kb)
(I used a web builder
 which you will need later for the lua compiler to build the LFS image)

Flash the firmware and connect to the NodeMCU using Esplorer
Create a init.lua file on the mcu to init wifi and mdns, and
set up LFS.

To install the lfs image for the first time, you must copy it to the
NodeMCU via usb-serial using Esplorer or similar. Subsequent updates
can be made by making the lfs.img available via http and calling
LFS.HTTP_OTA('servername', '/dir/', 'lfs.img')

Once lfs.img has first been copied to the NodeMCU, execute
node.flashreload('lfs.img')
and after it's rebooted, execute
pcall(node.flashindex('_init')())

Once LFS is set up, update the init.lua to do the flash _init call and
start the web IDE with LFS.ide()

Load the webIDE at http://xmas.local and create some scripts.
To play the animations, LFS.earth() returns a zero-indexed table
of every frame of the animation, each value in the table can
be written directly to ws2812.write(v)

