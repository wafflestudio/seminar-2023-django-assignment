# 과제 03: The large blog service with Django REST Framework

## 제출
- 제출 기한: 23. 11. 23(수) 23:59:59
- 제출 방법
  - 과제 진행한 Python project 폴더를 [./assignment](./assignment/) 폴더에 첨부해주세요.
  - 해당 repository를 fork하여 작업한 후, Pull Request를 날려주세요.
- 요구 사항
  - Blog, Post, Comment에 대해 각각 테스트 Instance 100개 이상을 생성해주세요.
  - AWS RDS, ElasticBeanstalk 등을 통해 API에 접속 가능한 환경을 만들어주세요.


## Requirements

여러분은 새로운 블로그의 Rest API를 설계해아 하는 한 스타트업의 서버 개발자가 되었습니다. 

이런! 협업할 서버 개발자는 따로 없습니다.

기획자이자 대표 C씨는 우리 블로그는 다른 서비스와 무언가 다를거라고 강조하면서, 다음과 같이 유저 스토리를 작성해주셨습니다. 하단 유저 스토리들을 하나씩 구현해나가야 합니다. 

### 유저 스토리
- [ ] User
  - [ ] Create  
    - [ ] 유저는 아이디와 비밀번호로 서비스에 가입할 수 있다.
    - [ ] 비밀번호는 hash된 상태로 DB 테이블에 저장되어야 한다.
- [ ] Admin 
  - [ ] admin user의 경우 모든 authentication을 무시하고 요청을 날릴 수 있어야 한다.
- [ ] Post 
  - [ ] Create
    - [ ] (인증) 비회원은 Post를 생성할 수 없고, 오직 회원만 가능하다.
    - [ ] 당연히 해당 내용들은 필요하다. 다른 내용도 필요할수도?: `created_by, created_at, updated_at, title, description`
  - [ ] List 
    - [ ] (인증) 회원 / 비회원 모두 리스트 요청을 날릴 수 있다.
    - [ ] Post 내용은 List 요청시 최대 앞 300자만 보낸다.
  - [ ] Detail 
    - [ ] (인증) 회원 / 비회원 모두 상세 요청을 날릴 수 있다.
  - [ ] Delete 
    - [ ] (인증) 작성한 사람만 해당 Post를 삭제할 수 있다.
  - [ ] Update 
    - [ ] (인증) 작성한 사람만 해당 Post를 수정할 수 있다.
- [ ] Comment
  - [ ] Create 
    - [ ] (인증) 비회원은 Comment를 생성할 수 없고, 오직 회원만 가능하다.
    - [ ] 당연히 해당 내용들은 필요하다. 다른 내용도 필요할수도?: `post, created_by, created_at, updated_at, content, is_updated`
  - [ ] Detail은 따로 없다.
  - [ ] List 
    - [ ] (인증) 회원 / 비회원 모두 리스트 요청을 날릴 수 있다.
    - [ ] Post id로 해당 post의 comment를 불러올 수 있다.
    - [ ] updated된 comment는 따로 `(수정됨)` 이 노출될 예정이므로, 해당 정보를 표시할 칼럼이 필요하다.
  - [ ] Update 
    - [ ] (인증) 작성한 사람만 수정할 수 있다.
  - [ ] Delete 
    - [ ] (인증) 작성한 사람만 삭제할 수 있다.

클라이언트는 우선 React 개발자인 R씨 한명입니다. R씨는 다음과 같이 요청했습니다.

- 인증을 server side에서 API별로 빡세게 구현해주세요. Frontend에서 인증 로직을 빡세게 걸진 않을거에요.
  - [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) 을 사용해주세요.
- Client error 시 참고할 error를 예쁘게 내려주세요. validation이 실패했는데 500이 나면 안됩니다.
- 모든 list 요청에는 무한 로딩을 적용할 거에요. 생성 역순으로 정렬해주시고, 이에 맞는 [cursor pagination](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination) 을 적용해주세요.
- 페이지 렌더시 필요한데요, 리스트 요청시와 상세 요청시의 정보는 달라야해요.
  - 리스트 요청시 무거운 내용이 함께 내려오면 안돼요. network 비용이 증가합니다.

디자이너 D씨는 서버 개발자가 대체 뭐하는 건지는 모르겠지만, 모든 클라이언트 로딩이 2초 이상 걸리지 않게 협조해달라고 요청했습니다.

### Tag 기능
C씨는 post에도, comment에도 태그를 달고 추후 이 태그로 알고리즘을 돌리는 게 large 블로그 서비스의 핵심 차별성이라고 하셨습니다.

- [ ] Tag 
  - [ ] Create
    - [ ] 따로 Tag를 생성하는 API는 없다. Post 생성, Comment 생성시 태그를 달고, 이 태그가 존재하지 않을시 생성된다.
    - [ ] tag content가 해당 tag의 id이자, primary key 이다.
    - [ ] 당연히 해당 내용들은 필요하다. 다른 내용도 필요할수도?: `content`
  - [ ] Tag update는 존재하지 않는다.
  - [ ] Delete
    - [ ] 따로 Tag를 삭제하는 API는 없다. Post / Comment 삭제시, 해당 Tag를 가진 Post나 Comment가 없을 경우 삭제된다.
  - [ ] Post list by tag
    - [ ] 해당 태그가 달린 Post List를 불러올 수 있다.
    - [ ] (인증) 회원 / 비회원 모두 Post list by tag를 불러올 수 있다.
  - [ ] Comment list by tag
    - [ ] 해당 태그가 달린 Comment List를 불러올 수 있다.
    - [ ] (인증) 회원 / 비회원 모두 Comment list by tag를 불러올 수 있다.


# 플립 러닝 03

### 세미나장 코멘트

> Django 관련된 강의는 모두 수강했으므로, 앞으로 필수로 수강해야 할 플립 러닝은 없습니다.
> 하지만 하단 내용을 잘 모르는 분은 수강하시기를 권장드려요!


## 선택 수강
- [SQL로 하는 데이터 관리](https://www.codeit.kr/topics/data-management-using-sql?pathSlug=sql-database-for-developers&categoryId=62c288e9672c77328d2aa4a7)
- [객체 지향 프로그래밍이란?](https://www.codeit.kr/topics/what-is-oop?pathSlug=object-oriented-programming-python&categoryId=62c288e9672c77328d2aa4a7)

