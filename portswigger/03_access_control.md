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
바디 파라미터에 "roleid"=2 를 추가하여 send 하면 됨.
그 open browser에서 연 페이지 말고 원래 페이지에서 공격하는거군.
어느 엔드포인트에서 proxy할건지 (파라미터가 어디 담겨있는지 등) 시도해보기!


