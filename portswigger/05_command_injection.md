Command Injection이 생기는 전형적인 구조는 사용자 입력값이 OS 명령의 인자(argument)로 들어가는 경우.

[portswigger] <OS Command injection via different responses>
goal: execute the whoami command to determine the name of the current user. 
풀이: Burp Suite Repeater로 인자 바꿔서 공격하는 것. 
productId=1 --> productId=1|whoami  (물론 인자 중 어디가 vulnerable할지 모름. 이 경우 둘다 취약했음.)

*url encoding: 구분자인지 그냥 데이터인지 구분되도록 16진수 아스키코드로 바꾸는 것. (내가 원하는 paylaod가 중간에 안잘리게) 즉, &를 쓴 이유는 os가 이거 보고 명령어로 받아들여줫음 좋겟는데 http가 자기들껀줄알고 먼저 파라미터에 써버리면 os까지 얘가 도달하지않아서. url 인코딩되면 http는 디코딩만 하고 shell로 보내니!!
16진수 아스키코드요??? -> 문자를 아스키번호로 변환. 그 번호를 16진수로 변환. 앞에 %만 붙임.
; : 앞 명령어 성공여부 상관 없이 뒤 명령어 
&& : 앞 명령어 성공하면
|| : 앞 명령어 실패하면
| : 앞 명령어의 결과를 뒤 명령어로

*훨씬 안전: subprocess.run(["ping", ip], shell=False)


[portswigger] Blind OS command injection with time delays
goal:blind os command injection으로 10 second delay 만들어라.
풀이: burp suite으로 파라미터 repeater 수정. 각 파라미터뒤에 < & sleep 10 #> 을 url 인코딩하여(%26%20sleep%2010%20%23) 응답이 10초만에 오는게 있는지 체크. email 파라미터가 취약했음. (blind라서 응답 command가 응답으로 안돌아옴!)
*shell 문법에서 띄어쓰기 신경써야함. sleep 10# 와 sleep 10 # 다름.
& sleep과 &sleep은 같음. shell이 &는 연산자로 구분가능한데 10#를 하나의 인자로 받아들일 수 있음.


[portswigger] Blind OS command injection with output redirection
goal: redirection을 통해 너가 입력한 command의 output을 capture해라. writable folder은 /var/www/images/에 있다. whomai를 실행하고, image loading URL을 사용하여 file의 content를 가져와라.
풀이: 여러 파라미터 중 취약했던 email 파라미터를 =||whoami>/var/www/images/output.txt|| 로 바꾼다. (whoami 명령어에 대한 결과를 저 output.txt에 저장) 이후 image loading url을 이용하랬으니 상품 이미지가 등록되는 페이지를 intercept하여 헤더를 GET /image?filename=output.txt HTTP/2 로 수정한다. (기존: GET /product?productId=2 HTTP/2)
