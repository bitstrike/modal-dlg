#!/bin/bash

# Path to the Python script
PYTHON_SCRIPT="./modal-dlg.py"

B_YES=-8
B_NO=-9
B_OK=-5

# Function to call the dialog and handle the response
test_dialog() {
    local buttons="$1"
    local icon="$2"
    local title="$3"
    local text="$4"
    local sound="$5"

    # Call the Python script and capture the output
    response=$($PYTHON_SCRIPT $buttons --icon "$icon" --title "$title" --text "$text" --yes --sound "$sound")

    # Extract the button value from the response
    button_value=$(echo "$response" | grep -oP 'Button clicked: \K.*')

    # Use a case statement to act on the button value
    case "$button_value" in
        $B_OK)
            echo "Ok button was clicked."
            ;;
        $B_YES)
            echo "Yes button was clicked."
            ;;
        $B_NO)
            echo "No button was clicked."
            ;;
        *)
            echo "Unknown button value: $button_value"
            ;;
    esac
}


# check if python sound module is installed
python3 -c "import playsound" &>/dev/null
result=$?

# Test the dialog with Yes, No, Ok buttons and sound, if available
if [ $result -eq 0 ]; then
    test_dialog "--yes --no --ok" "/usr/share/icons/Mint-Y/status/48/stock_dialog-info.png" "Test Dialog" "Click a button to test." "/usr/share/sounds/LinuxMint/stereo/dialog-information.ogg"
else
    test_dialog "--yes --no --ok" "/usr/share/icons/Mint-Y/status/48/stock_dialog-info.png" "Test Dialog" "Click a button to test."
fi

