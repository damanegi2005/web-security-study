*음 내느낌으로 엑세스컨트롤은 걍 다 버프수트같은걸로 요청 리퀘스트해서 파라미터 바꾸던지 해서 리피터 사용하는 느낌.

[portswigger] <Access Control- Unprotected admin functionality>
목적) delete the user carlos. (unprotected admin panel 갖고있음)
풀이)
robots.txt를 숨겨진 다이렉터리를 보는데 사용했대. 
 /robots.txt : 검색엔진에게 instructions를 주는 텍스트파일. "이경로는 크롤링해도돼/안돼" 알려주는. 생성된 파일. 보이고싶지 않은 경로들 여기적어서 제어. (엇 숨기는 바가 있군아)
아니면 brute force로.




[portswigger] <Access Control- Unprotected admin funtionality with unpredictable URL>
목적) unprotedted admin panel이 어딘가 있다. admin panel 접속해서 carlos user 삭제.
풀이) 소스코드 뒤져보기. admin 검색, certain logic 발견. admin panel 발견. 발견한 패널로 접속!




[portswigger] Cookie 조작해서 carlos 지우기
목적) admin panel 접근해서 carlos 지우자. wiener 계정으로 로그인 가능해.
풀이)
버프수트-http history보면 응답에 쿠키가 두개 있음. : 
Set-Cookie: session=70qRQW...    ← "너는 wiener야" (신원)
Set-Cookie: Admin=false          ← "너는 관리자 아니야" (권한)
여기서 true로 바꾸고
*
로그인 아예 못하면 session이 아예 없어서 wiener로 로그인한것.
풀이: 개발자도구 application -> cookie에서 admin 의 값을 false->true로 바꿈.
그러고 다시 admin 패널 시도.


[portswigger] User role can be modified in user profile
목적) roleid=2 로 접근하여 admin 패널 접속가능하게만들기
풀이) 버프수트 사용하여 /changeemail 리피터로 보내기. 그냥 send 바로 누르면 roleid=1임을 볼 수 있음. 
바디 파라미터에 <"roleid"=2> 를 추가!!하여 send 하면 됨.
그 open browser에서 연 페이지 말고 원래 페이지에서 공격하는거군.
어느 엔드포인트에서 proxy할건지 (파라미터가 어디 담겨있는지 등) 시도해보기!


[portswigger] User ID controlled by request parameter
(repeater 쓰는 개쉬운문제)
목적) carlos에 대한 API key 찾아라.
풀이) 내가 아는 wiener로 로그인해서 request를 intercept. 버프수트 리피터로 보내서 젤 위 헤더에 id=wiener를 id=carlos로 바꾸고 send. 응답에서 찾으면 됨.

[portswigger] " with unpredictable user IDs
목적) find the GUID for carlos, and API key 찾아라.
풀이) 게시글중 carlos꺼 찾아. carlos 누르고 그때 뜨는 userid로 내 id를 바꿔(버프수트)
*즉 다 똑같음. 중간에 가로채서 파라미터 바꾸는거. 대신 carlos의 파라미터 알 방도가 없으니 직접 게시물 찾자!!ㅎㅎ
