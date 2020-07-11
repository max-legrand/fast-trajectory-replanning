# Using applescript, sets the focus + foreground on a window by its title
# That works on OSX 10.7.5.
# @author Aurelien Scoubeau <aurelien.scoubeau@gmail.com>
# @lastChangedBy Max Legrand
import subprocess


def focus_title(title):
    # find the app or window back and activate it
    apple = """
    set the_title to "%s"
    tell application "System Events"
        repeat with p in every process whose background only is false
            repeat with w in every window of p
                if (name of w) is the_title then
                    tell p
                        set frontmost to true
                        perform action "AXRaise" of w
                    end tell
                end if
            end repeat
        end repeat
    end tell
    """ % (title,)
    apple = bytes(apple, "utf8")
    p = subprocess.Popen(
        'osascript',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    p.communicate(apple)[0]


def focus_app(title):
    # find the app or window back and activate it
    apple = """
    set the_title to "%s"
    tell application "System Events"
        repeat with p in every process whose background only is false
            if (name of p) is the_title then
                tell p
                    set frontmost to true
                    perform action "AXRaise" of w
                end tell
            end if
        end repeat
    end tell
    """ % (title,)
    apple = bytes(apple, "utf8")
    p = subprocess.Popen(
        'osascript',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    p.communicate(apple)[0]


if __name__ == "__main__":
    focus_title("A Star")
