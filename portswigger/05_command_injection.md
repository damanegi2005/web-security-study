7. <OS Command injection via different responses>
goal: execute the whoami command to determine the name of the current user. 

**Burp Suite Repeater로 인자 바꿔서 공격하는 것. 
productId=1 --> productId=1|whoami  (물론 인자 중 어디가 vulnerable할지 모름)

*url encoding: 구분자인지 그냥 데이터인지 구분되도록 16진수 아스키코드로 바꾸는 것. (내가 원하는 paylaod가 중간에 안잘리게)
16진수 아스키코드요??? -> 문자를 아스키번호로 변환. 그 번호를 16진수로 변환. 앞에 %만 붙임.
