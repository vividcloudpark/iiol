# Generated by Django 4.0.5 on 2023-09-11 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BigRegion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('DELETED', models.BooleanField(null=True)),
                ('big_region_code', models.CharField(choices=[('11', '서울특별시'), ('21', '부산광역시'), ('22', '대구광역시'), ('23', '인천광역시'), ('24', '광주광역시'), ('25', '대전광역시'), ('26', '울산광역시'), ('29', '세종특별자치시'), ('31', '경기도'), ('32', '강원도'), ('33', '충청북도'), ('34', '충청남도'), ('35', '전라북도'), ('36', '전라남도'), ('37', '경상북도'), ('38', '경상남도'), ('39', '제주특별자치도')], max_length=2, primary_key=True, serialize=False)),
                ('big_region_name', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['big_region_code'],
            },
        ),
        migrations.CreateModel(
            name='SmallRegion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('DELETED', models.BooleanField(null=True)),
                ('small_region_code', models.CharField(choices=[('11010', '종로구'), ('11020', '중구'), ('11030', '용산구'), ('11040', '성동구'), ('11050', '광진구'), ('11060', '동대문구'), ('11070', '중랑구'), ('11080', '성북구'), ('11090', '강북구'), ('11100', '도봉구'), ('11110', '노원구'), ('11120', '은평구'), ('11130', '서대문구'), ('11140', '마포구'), ('11150', '양천구'), ('11160', '강서구'), ('11170', '구로구'), ('11180', '금천구'), ('11190', '영등포구'), ('11200', '동작구'), ('11210', '관악구'), ('11220', '서초구'), ('11230', '강남구'), ('11240', '송파구'), ('11250', '강동구'), ('21010', '중구'), ('21020', '서구'), ('21030', '동구'), ('21040', '영도구'), ('21050', '부산진구'), ('21060', '동래구'), ('21070', '남구'), ('21080', '북구'), ('21090', '해운대구'), ('21100', '사하구'), ('21110', '금정구'), ('21120', '강서구'), ('21130', '연제구'), ('21140', '수영구'), ('21150', '사상구'), ('21310', '기장군'), ('22010', '중구'), ('22020', '동구'), ('22030', '서구'), ('22040', '남구'), ('22050', '북구'), ('22060', '수성구'), ('22070', '달서구'), ('22310', '달성군'), ('23010', '중구'), ('23020', '동구'), ('23030', '남구'), ('23040', '연수구'), ('23050', '남동구'), ('23060', '부평구'), ('23070', '계양구'), ('23080', '서구'), ('23310', '강화군'), ('23320', '옹진군'), ('24010', '동구'), ('24020', '서구'), ('24030', '남구'), ('24040', '북구'), ('24050', '광산구'), ('25010', '동구'), ('25020', '중구'), ('25030', '서구'), ('25040', '유성구'), ('25050', '대덕구'), ('26010', '중구'), ('26020', '남구'), ('26030', '동구'), ('26040', '북구'), ('26310', '울주군'), ('29010', '세종시'), ('31010', '수원시'), ('31011', '수원시 장안구'), ('31012', '수원시 권선구'), ('31013', '수원시 팔달구'), ('31014', '수원시 영통구'), ('31020', '성남시'), ('31021', '성남시 수정구'), ('31022', '성남시 중원구'), ('31023', '성남시 분당구'), ('31030', '의정부시'), ('31040', '안양시'), ('31041', '안양시 만안구'), ('31042', '안양시 동안구'), ('31050', '부천시'), ('31060', '광명시'), ('31070', '평택시'), ('31080', '동두천시'), ('31090', '안산시'), ('31091', '안산시 상록구'), ('31092', '안산시 단원구'), ('31100', '고양시'), ('31101', '고양시 덕양구'), ('31103', '고양시 일산동구'), ('31104', '고양시 일산서구'), ('31110', '과천시'), ('31120', '구리시'), ('31130', '남양주시'), ('31140', '오산시'), ('31150', '시흥시'), ('31160', '군포시'), ('31170', '의왕시'), ('31180', '하남시'), ('31190', '용인시'), ('31191', '용인시 처인구'), ('31192', '용인시 기흥구'), ('31193', '용인시 수지구'), ('31200', '파주시'), ('31210', '이천시'), ('31220', '안성시'), ('31230', '김포시'), ('31240', '화성시'), ('31250', '광주시'), ('31260', '양주시'), ('31270', '포천시'), ('31280', '여주시'), ('31350', '연천군'), ('31370', '가평군'), ('31380', '양평군'), ('32010', '춘천시'), ('32020', '원주시'), ('32030', '강릉시'), ('32040', '동해시'), ('32050', '태백시'), ('32060', '속초시'), ('32070', '삼척시'), ('32310', '홍천군'), ('32320', '횡성군'), ('32330', '영월군'), ('32340', '평창군'), ('32350', '정선군'), ('32360', '철원군'), ('32370', '화천군'), ('32380', '양구군'), ('32390', '인제군'), ('32400', '고성군'), ('32410', '양양군'), ('33020', '충주시'), ('33030', '제천시'), ('33040', '청주시'), ('33041', '청주시 상당구'), ('33042', '청주시 서원구'), ('33043', '청주시 흥덕구'), ('33044', '청주시 청원구'), ('33320', '보은군'), ('33330', '옥천군'), ('33340', '영동군'), ('33350', '진천군'), ('33360', '괴산군'), ('33370', '음성군'), ('33380', '단양군'), ('33390', '증평군'), ('34010', '천안시'), ('34011', '천안시 동남구'), ('34012', '천안시 서북구'), ('34020', '공주시'), ('34030', '보령시'), ('34040', '아산시'), ('34050', '서산시'), ('34060', '논산시'), ('34070', '계룡시'), ('34080', '당진시'), ('34310', '금산군'), ('34330', '부여군'), ('34340', '서천군'), ('34350', '청양군'), ('34360', '홍성군'), ('34370', '예산군'), ('34380', '태안군'), ('35010', '전주시'), ('35011', '전주시 완산구'), ('35012', '전주시 덕진구'), ('35020', '군산시'), ('35030', '익산시'), ('35040', '정읍시'), ('35050', '남원시'), ('35060', '김제시'), ('35310', '완주군'), ('35320', '진안군'), ('35330', '무주군'), ('35340', '장수군'), ('35350', '임실군'), ('35360', '순창군'), ('35370', '고창군'), ('35380', '부안군'), ('36010', '목포시'), ('36020', '여수시'), ('36030', '순천시'), ('36040', '나주시'), ('36060', '광양시'), ('36310', '담양군'), ('36320', '곡성군'), ('36330', '구례군'), ('36350', '고흥군'), ('36360', '보성군'), ('36370', '화순군'), ('36380', '장흥군'), ('36390', '강진군'), ('36400', '해남군'), ('36410', '영암군'), ('36420', '무안군'), ('36430', '함평군'), ('36440', '영광군'), ('36450', '장성군'), ('36460', '완도군'), ('36470', '진도군'), ('36480', '신안군'), ('37010', '포항시'), ('37011', '포항시 남구'), ('37012', '포항시 북구'), ('37020', '경주시'), ('37030', '김천시'), ('37040', '안동시'), ('37050', '구미시'), ('37060', '영주시'), ('37070', '영천시'), ('37080', '상주시'), ('37090', '문경시'), ('37100', '경산시'), ('37310', '군위군'), ('37320', '의성군'), ('37330', '청송군'), ('37340', '영양군'), ('37350', '영덕군'), ('37360', '청도군'), ('37370', '고령군'), ('37380', '성주군'), ('37390', '칠곡군'), ('37400', '예천군'), ('37410', '봉화군'), ('37420', '울진군'), ('37430', '울릉군'), ('38030', '진주시'), ('38050', '통영시'), ('38060', '사천시'), ('38070', '김해시'), ('38080', '밀양시'), ('38090', '거제시'), ('38100', '양산시'), ('38110', '창원시'), ('38111', '창원시 의창구'), ('38112', '창원시 성산구'), ('38113', '창원시 마산합포구'), ('38114', '창원시 마산회원구'), ('38115', '창원시 진해구'), ('38310', '의령군'), ('38320', '함안군'), ('38330', '창녕군'), ('38340', '고성군'), ('38350', '남해군'), ('38360', '하동군'), ('38370', '산청군'), ('38380', '함양군'), ('38390', '거창군'), ('38400', '합천군'), ('39010', '제주시'), ('39020', '서귀포')], db_index=True, max_length=5, primary_key=True, serialize=False)),
                ('small_region_name', models.CharField(max_length=10)),
                ('big_region_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.bigregion')),
            ],
            options={
                'ordering': ['small_region_code'],
            },
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('DELETED', models.BooleanField(null=True)),
                ('libcode', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('libName', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('tel', models.CharField(max_length=50)),
                ('fax', models.CharField(max_length=50)),
                ('latitue', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('homepage', models.URLField()),
                ('closed', models.CharField(max_length=50)),
                ('operatingTime', models.CharField(max_length=50)),
                ('big_region_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.bigregion')),
                ('small_region_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.smallregion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]