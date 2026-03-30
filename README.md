# PHD 알람 발송
PHD → EventBridge → SNS → Lambda → SpaceONE → MS Teams
## Lambda
- SNS를 타고 들어온 데이터 파싱
  - account 필드를 affectedAccount 필드로 교체
