; Inno Setup script — Project IChing
; 需先執行 packaging\build_exes.ps1 產生 dist\IChing 與 dist\IChingDataEditor
; 再用 Inno Setup Compiler 編譯本檔

#define MyAppName "Project IChing"
#define MyAppVersion "1.4.10"
#define MyAppPublisher "IChing"
#define MyAppExeName "IChing.exe"
#define MyEditorExeName "IChingDataEditor.exe"

[Setup]
AppId={{8F3C2A1B-6D4E-4F90-9B21-ICHING1410}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\IChing
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=..\dist\installer
OutputBaseFilename=IChingSetup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "建立桌面捷徑"; GroupDescription: "其他選項:"; Flags: unchecked

[Files]
; 主程式（onedir）
Source: "..\dist\IChing\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Data Editor 獨立子目錄，避免 _internal 衝突
Source: "..\dist\IChingDataEditor\*"; DestDir: "{app}\DataEditor"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\IChing Data Editor"; Filename: "{app}\DataEditor\{#MyEditorExeName}"
Name: "{group}\解除安裝 {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\IChing Data Editor"; Filename: "{app}\DataEditor\{#MyEditorExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "啟動 {#MyAppName}"; Flags: nowait postinstall skipifsilent
