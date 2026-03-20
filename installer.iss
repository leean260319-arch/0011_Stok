; StokAI Inno Setup 인스톨러 스크립트
; 컴파일: "C:\Users\USER\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer.iss
;
; v1.1 - 2026-03-17: Windows Defender 제외, 방화벽 규칙, SmartScreen 우회 추가

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName=StokAI
AppVersion=0.1.0
AppVerName=StokAI 0.1.0
AppPublisher=StokAI
DefaultDirName={autopf}\StokAI
DefaultGroupName=StokAI
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=StokAI_Setup_0.1.0
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; SetupIconFile=assets\stokai.ico  ; 아이콘 파일이 있으면 주석 해제
UninstallDisplayIcon={app}\StokAI.exe
WizardStyle=modern
PrivilegesRequired=admin
; SmartScreen 관련: 서명 없는 exe에 대한 안내
InfoBeforeFile=dist\INSTALL_NOTE.txt

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "firewall"; Description: "Windows 방화벽에 웹 대시보드 포트(8080) 허용 규칙 추가"
Name: "defender"; Description: "Windows Defender 제외 경로에 설치 폴더 등록"

[Files]
; PyInstaller onedir 출력 전체를 설치 디렉토리에 복사
Source: "dist\StokAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; 시작 메뉴 바로가기
Name: "{group}\StokAI"; Filename: "{app}\StokAI.exe"
Name: "{group}\StokAI 제거"; Filename: "{uninstallexe}"
; 바탕화면 바로가기
Name: "{commondesktop}\StokAI"; Filename: "{app}\StokAI.exe"; Tasks: desktopicon

[Run]
; 1) Windows Defender 제외 경로 등록 (설치 폴더 + exe)
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Add-MpPreference -ExclusionPath '{app}'"""; StatusMsg: "Windows Defender 제외 경로 등록 중..."; Flags: runhidden waituntilterminated; Tasks: defender
; 2) Windows 방화벽 인바운드 규칙 추가 (웹 대시보드 TCP 8080)
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""StokAI Web Dashboard"" dir=in action=allow protocol=TCP localport=8080 program=""{app}\StokAI.exe"""; StatusMsg: "방화벽 규칙 추가 중..."; Flags: runhidden waituntilterminated; Tasks: firewall
; 3) Windows 방화벽 아웃바운드 규칙 추가
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""StokAI Outbound"" dir=out action=allow program=""{app}\StokAI.exe"""; Flags: runhidden waituntilterminated; Tasks: firewall
; 4) SmartScreen 실행 차단 방지: Zone.Identifier ADS 제거
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Get-ChildItem -Path '{app}' -Recurse | Unblock-File -ErrorAction SilentlyContinue"""; StatusMsg: "SmartScreen 차단 해제 중..."; Flags: runhidden waituntilterminated
; 5) 설치 완료 후 실행 옵션
Filename: "{app}\StokAI.exe"; Description: "StokAI 실행"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; 제거 시 방화벽 규칙 삭제
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""StokAI Web Dashboard"""; Flags: runhidden
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""StokAI Outbound"""; Flags: runhidden
; 제거 시 Defender 제외 해제
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Remove-MpPreference -ExclusionPath '{app}'"""; Flags: runhidden

[Code]
// 설치 전 기존 WDAC/AppLocker 정책 확인 안내
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // 설치 완료 후 추가 작업이 필요하면 여기서 실행
    Log('StokAI 설치 완료: Windows Defender 제외 및 방화벽 규칙 등록됨');
  end;
end;
