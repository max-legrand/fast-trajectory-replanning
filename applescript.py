# Using AppleScript, lists the title of every window.
# If an hint is given, the list filtered using fuzzy matching.
# That works on OSX 10.7.5.
# @author Aurelien Scoubeau <aurelien.scoubeau@gmail.com>
# @lastChangedBy Max Legrand
import subprocess


possibilities = []
apple = b"""
set window_titles to {}
tell application "System Events"
    repeat with p in every process whose background only is false
        repeat with w in every window of p
            set end of window_titles to (name of p) & "|>" & (name of w)
        end repeat
    end repeat
end tell
set AppleScript's text item delimiters to "\n"
window_titles as text
"""
p = subprocess.Popen('osascript',
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
windows = p.communicate(apple)[0].decode('utf8').split('\n')

for c in windows:
    print(c.encode('utf8'))
