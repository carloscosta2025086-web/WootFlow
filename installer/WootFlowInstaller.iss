#define MyAppName "WootFlow"
#ifndef AppVersion
  #define AppVersion "0.0.0-local"
#endif
#ifndef RepoDir
  #define RepoDir "."
#endif
#ifndef SourceDir
  #define SourceDir "dist\WootingRGB"
#endif
#define MyAppPublisher "Carlos Costa"
#define MyAppURL "https://github.com/carloscosta2025086-web/WootFlow"
#define MyAppExeName "WootingRGB.exe"
#define MyAppId "{{B7A6E3A8-4A98-49E2-BAF0-5B4EA52F7D91}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#AppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\WootFlow
DefaultGroupName=WootFlow
AllowNoIcons=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupLogging=yes

OutputDir={#RepoDir}\installer\output
OutputBaseFilename=WootFlow-Setup-{#AppVersion}
UninstallDisplayIcon={app}\assets\wootflow_icon.ico
DisableProgramGroupPage=yes
ChangesEnvironment=no

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho no ambiente de trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "wootflow_debug.log"
Source: "{#RepoDir}\installer\prereqs\vc_redist.x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall skipifsourcedoesntexist
Source: "{#RepoDir}\installer\prereqs\MicrosoftEdgeWebView2RuntimeInstallerX64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall skipifsourcedoesntexist
Source: "{#RepoDir}\installer\prereqs\MicrosoftEdgeWebView2Setup.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall skipifsourcedoesntexist


[Icons]
Name: "{group}\WootFlow"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\wootflow_icon.ico"
Name: "{group}\Desinstalar WootFlow"; Filename: "{uninstallexe}"; IconFilename: "{app}\assets\wootflow_icon.ico"
Name: "{autodesktop}\WootFlow"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon; IconFilename: "{app}\assets\wootflow_icon.ico"

[Run]
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/install /quiet /norestart"; StatusMsg: "A instalar Microsoft Visual C++ Redistributable..."; Flags: waituntilterminated; Check: NeedsVCRedist and FileExists(ExpandConstant('{tmp}\vc_redist.x64.exe'))
Filename: "{tmp}\MicrosoftEdgeWebView2RuntimeInstallerX64.exe"; Parameters: "/silent /install"; StatusMsg: "A instalar Microsoft Edge WebView2 Runtime..."; Flags: waituntilterminated; Check: NeedsWebView2 and FileExists(ExpandConstant('{tmp}\MicrosoftEdgeWebView2RuntimeInstallerX64.exe'))
Filename: "{tmp}\MicrosoftEdgeWebView2Setup.exe"; Parameters: "/silent /install"; StatusMsg: "A instalar Microsoft Edge WebView2 Runtime..."; Flags: waituntilterminated; Check: NeedsWebView2 and (not FileExists(ExpandConstant('{tmp}\MicrosoftEdgeWebView2RuntimeInstallerX64.exe'))) and FileExists(ExpandConstant('{tmp}\MicrosoftEdgeWebView2Setup.exe'))
Filename: "{app}\{#MyAppExeName}"; Description: "Executar WootFlow agora"; Flags: nowait postinstall skipifsilent unchecked

[Code]
function HasRegStringValue(const RootKey: Integer; const SubKey, ValueName: String): Boolean;
var
  Data: String;
begin
  Result := RegQueryStringValue(RootKey, SubKey, ValueName, Data) and (Data <> '') and (Data <> '0.0.0.0');
end;

function NeedsWebView2: Boolean;
begin
  Result :=
    not HasRegStringValue(HKLM, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv') and
    not HasRegStringValue(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv') and
    not HasRegStringValue(HKCU, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv');
end;

function NeedsVCRedist: Boolean;
var
  Installed: Cardinal;
  Major: Cardinal;
begin
  Result := True;

  if RegQueryDWordValue(HKLM, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Installed', Installed) and
     RegQueryDWordValue(HKLM, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Major', Major) then
  begin
    if (Installed = 1) and (Major >= 14) then
    begin
      Result := False;
      exit;
    end;
  end;

  if RegQueryDWordValue(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Installed', Installed) and
     RegQueryDWordValue(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Major', Major) then
  begin
    if (Installed = 1) and (Major >= 14) then
      Result := False;
  end;
end;
