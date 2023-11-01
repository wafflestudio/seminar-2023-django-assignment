## The large blog service

![미디엄 대안](./medium-alternative.webp)

여러분은 새로운 블로그를 만드는 개발자가 되었습니다. 

---

하단 유저 스토리들을 하나씩 구현해나가야 합니다. 

### 유저 스토리
- [ ] Auth
  - [ ] Create Page
    - [ ] 유저는 아이디와 비밀번호로 서비스에 가입할 수 있다.
  - [ ] Login Page
    - [ ] 유저는 아이디와 비밀번호로 서비스에 로그인할 수 있다.
  - [ ] Logout Page
    - [ ] 버튼을 클릭하면 유저는 로그아웃 할 수 있다.
- [ ] Blog
  - [ ] Post Create Page
    - [ ] 글을 생성하는 페이지.
    - [ ] (인증) 비회원은 Post를 생성할 수 없고, 오직 회원만 가능하다.
  - [ ] Post List Page
    - [ ] 글 목록을 확인하는 페이지.
    - [ ] (인증) 회원 / 비회원 모두 리스트 요청을 날릴 수 있다.
    - [ ] Post 제목만 확인할 수 있고, 클릭 시 Detail Page로 연결된다.
  - [ ] Post Detail Page
    - [ ] 글 상세를 확인하고, 댓글을 작성하고, 글을 삭제할 수 있는 페이지.
    - [ ] (인증) 회원 / 비회원 모두 확인이 가능하다.
    - [ ] (인증) 비회원에게는 댓글 폼이 보이지 않지만, 댓글 목록 확인은 가능하다.
    - [ ] (인증) Post 작성자는 해당 글을 삭제할 수 있다.
  - [ ] Post Update Page 
    - [ ] 글을 수정할 수 있는 페이지.
    - [ ] (인증) 작성한 사람만 해당 글을 수정할 수 있다.
---

AWS RDS를 elastic beanstalk에 연동해, hosted 된 database를 사용해주세요.
[AWS 문서 참고](https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html)