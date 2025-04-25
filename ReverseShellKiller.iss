[Setup]
AppName=ReverseShellKiller
AppVersion=1.0
DefaultDirName={pf}\ReverseShellKiller
DefaultGroupName=ReverseShellKiller
OutputBaseFilename=ReverseShellKillerSetupInstaller
Compression=lzma
SolidCompression=yes
[Files]
Source: "C:\Users\butta\OneDrive\Desktop\ReverseShellKiller\dist\ReverseShellKiller.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\ReverseShellKillerSetup"; Filename: "{app}\ReverseShellKillerSetup.exe"
Name: "{group}\Uninstall ReverseShellKillerSetup"; Filename: "{uninstallexe}"
