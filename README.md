# Django-REST-making-APIs-backend-for-a-Lotto-game

## API endpoints:

- POST /lottos/ - User with manager IP can create a lotto with prizes 
- GET /lottos/ - All Lottos are shown
- GET /lottos/<id>/ - Get detail of a specific lotto
- POST /lottos/<id>/participate/ - All users can get a lotto with a random lotto number and a verification code (each user can get only one lotto)
- POST /lottos/<id>/winners/ - User with manager IP can draw the winners
- GET /lottos/<id>/winners/ - All users can check the winners
- POST /lottos/<id>/verify-ticket/ - Verify winners with the verification codes.
