import Widget from 'resource:///com/github/Aylur/ags/widget.js';
import { execAsync } from 'resource:///com/github/Aylur/ags/utils.js';
import { MaterialIcon } from '../.commonwidgets/materialicon.js'; // Assuming MaterialIcon utility is already in place
const { Box } = Widget;
let activeButton = null; // Variable to track the active button

// Function to fetch the current power profile
const getCurrentPowerProfile = async () => {
    try {
        const output = await execAsync('powerprofilesctl get');
        return output.trim(); // Clean the output to get the profile name
    } catch (error) {
        return 'unknown'; // Default in case of an error
    }
};

// Function to create a button and set it active if it matches the current profile
const createProfileButton = async (profileName, tooltipText, iconName, command) => {
    const currentProfile = await getCurrentPowerProfile();
    
    const button = Widget.Button({
        className: 'txt-small sidebar-iconbutton',
        tooltipText: getString(tooltipText), // Assuming getString is implemented elsewhere
        onClicked: (btn) => {
            execAsync(`powerprofilesctl set ${command}`).catch(print);
            btn.toggleClassName('sidebar-button-active', true);

            // Deactivate previously active button if any
            if (activeButton && activeButton !== btn) {
                activeButton.toggleClassName('sidebar-button-active', false);
            }

            // Update the active button reference
            activeButton = btn;
        },
        child: MaterialIcon(iconName, 'norm'), // Assuming MaterialIcon returns Pixbuf or string
    });

    // Set the button as active if it matches the current profile
    if (currentProfile === profileName) {
        button.toggleClassName('sidebar-button-active', true);
        activeButton = button;
    }

    return button;
};

// Balanced Profile Module
export const BalancedProfile = async (props = {}) => {
    return createProfileButton('balanced', 'Balanced', 'settings_suggest', 'balanced');
};

// PowerSave Profile Module
export const PowerSaveProfile = async (props = {}) => {
    return createProfileButton('power-saver', 'PowerSave', 'battery_saver', 'power-saver');
};

// Performance Profile Module
export const PerformanceProfile = async (props = {}) => {
    return createProfileButton('performance', 'Performance', 'flash_on', 'performance');
};

// Title for Power Profile with Icon
export const PowerProfileTitle = async () => {
    return Widget.Box({
        className: 'spacing-h-10 txt',
        children: [
            MaterialIcon('settings_power', 'norm'),
            Widget.Label({
                label: getString('Set Power Profile:'), // Assuming getString is implemented elsewhere
                className: 'txt-medium txt', // You can customize this class for styling
                halign: 'center',
            }),
        ],
    });
};

// Check if powerprofilesctl is available
async function createPowerBox() {
    try {
        const powerProfilesCtlAvailable = await execAsync('which powerprofilesctl');

        if (!powerProfilesCtlAvailable || powerProfilesCtlAvailable.trim().length === 0) {
            return null;  // If powerprofilesctl is not available, return null
        }

        const powerTitle = Box({
            className: 'spacing-h-5 txt-medium sidebar-group-invisible-morehorizpad',
            children: [
                await PowerProfileTitle(),
            ],
        });

        // Create the power profile button box
        const powerBox = Box({
            className: 'spacing-h-5 txt-medium',
            children: [
                Widget.Box({
                    hpack: 'center',
                    className: 'spacing-h-5',
                    children: [
                        await BalancedProfile(),
                        await PowerSaveProfile(),
                        await PerformanceProfile(),
                    ],
                }),
            ],
        });

        // Create a parent box to hold both title and power box side by side and stretch across the full width
        const powerModule = Box({
            className: 'spacing-h-10 power-module',
            children: [
                powerTitle,
                Widget.Box({ hexpand: true }),
                powerBox,
            ],
        });

        // Return the entire module with title and power box in a single layout
        return powerModule;
    } catch (error) {
        console.log('Error: powerprofilesctl check failed:', error);
        return null;  // In case of any errors, return null
    }
}

// Use the function to add the widget to the interface only if power profiles daemon is available via powerprofilesctl
export const powerModule = await createPowerBox();

