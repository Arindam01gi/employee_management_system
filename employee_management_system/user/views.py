# type: ignore
from rest_framework import viewsets, request
from rest_framework.decorators import action, api_view
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.utils import json
from django.db import transaction
from django.conf import settings
from django.db import connection
from datetime import datetime
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from constant import *
from errors import *
from .utils import (getMd5Hash)
from .models import (UserDetails,User)
from shared.models import (DomainLookup)
from .serializers import UserDetailsSerializer,PostSerializer

import logging, re, dateutil, hashlib, base64, pytz, math, mimetypes
import json, sys

# Create your views here.

logger = logging.getLogger(__name__)
timeZ_Ind = pytz.timezone('Asia/Kolkata')

''' User Health Check '''


@api_view(['GET'])
def getAdminHealth(request):
    logger.info("< =================== Project Employee Management System is OK =================== >\n")
    cur_time = datetime.now(pytz.utc)
    utc_time = cur_time.replace(tzinfo=pytz.utc)
    dateonly = utc_time.date()
    timeonly = utc_time.time()
    timeonly = timeonly.strftime("%I:%M %p")

    # logger.info(f"The current Date-Time is >> {utc_time} OR {dateonly} {timeonly}\n")

    # local_timezone = tzlocal.get_localzone()
    local_timezone = dateutil.tz.gettz('Asia/Calcutta')
    ist_time = cur_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    # ist_time = cur_time.replace(tzinfo=pytz.utc)
    ist_dateonly = ist_time.date()
    ist_timeonly = ist_time.time()
    ist_timeonly = ist_timeonly.strftime("%I:%M %p")

    isttime = {"date": f"{ist_dateonly} IST", "time": f"{ist_timeonly} IST"}
    utctime = {"date": f"{dateonly}", "time": f"{timeonly} UTC"}

    output = {"Module": "user", "condition": "OK",
              "UTC Timezone": utctime, "IST Timezone": isttime}

    logger.info("< =================== User Health Check Response Complete =================== >\n")
    return Response(output)


@api_view(['POST'])
def addUser(request):
    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []
    logger.info("<========== USER ADD ====>")
    try:
        data = request.data
        logger.info(f"Requested Data = {data}")
        user_id = data['user_id'] if data.get('user_id') else None
        username = data['username'] if data.get('username') else None
        user_role = data['user_role'] if data.get('user_role') else None
        password = data['password'] if data.get('password') else None
        firstname = data['firstname'] if data.get('firstname') else None
        lastname = data['lastname'] if data.get('lastname') else None
        email = data['email'] if data.get('email') else None
        phone = data['phone'] if data.get('phone') else None
        profile_pic = data['profile_pic'] if data.get('profile_pic') else None
        salary = data['salary'] if data.get('salary') else None
        joining_date = data['joining_date'] if data.get('joining_date') else None
        designation = data['designation'] if data.get('designation') else None
        org_id = data['org_id'] if data.get('org_id') else None

        if (username is None or username == '') or (password is None or password == '') or (firstname is None or firstname == '') or (phone is None or phone == '') or (email is None or email == '') or(user_role is None or user_role=='') or org_id in(None,''):
            raise MandatoryInputMissingException('Mandetory Input Missing')
        
        if(len(password)<3 or len(password)> 20):
            logger.error("Password length must be between 3 to 20")
            raise CharacterLengthException('Length must be between 3 to 20')
        else:
            logger.info("Password length statisfied")
            passwordmd5 = getMd5Hash(password)
            if passwordmd5 is None:
                raise OperationalException("Failed to generate MD5 hash")
            
        phone_email_valid = None
        phone_email_exists = None
        
        if phone is not None:
            if re.match(r"^[123456789]{1}\d{9}$", phone):
                logger.info("Phone number format is valid")
                phone_exists = any(UserDetails.objects.raw(f"SELECT * FROM user_details WHERE BINARY phone = '{phone}'"))
                if phone_exists:
                    if user_id not in (None,''):
                        logger.info("User ID Available. Phone also exists")
                    else:
                        phone_email_exists = 1
                        raise PhoneEmailExistsException('Phone Number Already Exists')
                else:
                    logger.info("Phone Number Does not Exists in System")
                    if user_id not in (None,''):
                        logger.info("User ID Available. Phone not available")
            else:
                phone_email_valid = 1
                raise InvalidPhoneEmailFormat('Invalid Phone/Email Format')
            
        if email is not None:
            if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",email):
                logger.info("Email Address format is valid")
                email_exists = any(UserDetails.objects.raw(f"SELECT * FROM user_details WHERE BINARY email = '{email}'"))
                if email_exists:
                    if user_id not in (None,''):
                        logger.info("User ID Available. Email also exists")
                    else:
                        phone_email_exists = 2
                        raise PhoneEmailExistsException('Email Already Exists')
                else:
                    logger.info('Email Does not Exists in System')
                    if user_id not in (None,''):
                        logger.info("User ID Available. Email not available")
            else:
                phone_email_valid = 2
                raise InvalidPhoneEmailFormat('Invalid Phone/Email Format')
            
        user_data = {"username": username , "password":passwordmd5,"active":1}
        user_details_data = { "firstname":firstname ,"lastname":lastname,"user_role":user_role,"phone":phone,"email":email,"profile_pic":profile_pic,"salary":salary,"joining_date":joining_date,"designation":designation,"org_id":org_id }
        
        with transaction.atomic():
            logger.info(f"user id == {user_id}")
            if user_id not in (None,''):
                logger.info('Updating User Details')
                user_data['updated_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                User.objects.filter(user_id=user_id).update(**user_data)
                user_instance = User.objects.filter(user_id=user_id).get()
                user_details_data['user'] = user_instance
                user_details_data['updated_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                UserDetails.objects.filter(user_id = user_id).update(**user_details_data)
                logger.info('Successfully updated user information')
            else:
                logger.info("Creating user details")
                user_data['created_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                user_data['updated_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                user_data_create = User.objects.create(**user_data)
                user_id = user_data_create.user_id
                user_instance = User.objects.filter(user_id=user_id).get()
                user_details_data['user'] = user_instance
                user_details_data['created_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                user_details_data['updated_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                UserDetails.objects.create(**user_details_data)
                logger.info("User created succesfully")
                
            response_body = {
            'status': SUCCESSSTATUS,
            'success': "true",
            # 'message': "Record found.",
            'data': data
            }
                
            return Response(response_body)
                
        

    except MandatoryInputMissingException as mime:
        logger.exception(mime)
        ec.append(BE001)
        ec.append(BE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
    except CharacterLengthException as cle:
        logger.exception(cle)
        ec.append(BE002)
        ec.append(BE002MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
    except OperationalException as oe:
        logger.exception(oe)
        ec.append(IN001)
        ec.append(IN001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[0].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
    except PhoneEmailExistsException as peee:
        logger.exception(peee)
        ec.append(BE003)
        if phone_email_exists == 1:
            ec.append(BE003MESSAGE.format("Phone Number"))
        if phone_email_exists == 2:
            ec.append(BE003MESSAGE.format("Email"))
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[0].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
    except InvalidPhoneEmailFormat as ipee:
        logger.exception(ipee)
        ec.append(BE004)
        if phone_email_valid == 1:
            ec.append(BE004MESSAGE.format("Phone Number"))
        if phone_email_valid == 2:
            ec.append(BE004MESSAGE.format("Email"))
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[0].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})


    except Exception as e:
        logger.exception(e)
        ec.append(SE001)
        ec.append(SE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[3].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
@api_view(['POST'])
def userLogin(request):
    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []
    logger.info("<======================== Start - User Login ========================>")
    try:
        data = request.data
        logger.info(f"Requested Data = {data}")
        username=data['username'] if data.get('username') else None
        password=data['password'] if data.get('password') else None
        
        if (username is None or username == '') or (password is None or password == ''):
            raise MandatoryInputMissingException("Username/Password Missing")
        else:
            username_exist = User.objects.filter(username=username).exists()
            logger.info(f"Exists ->{username_exist}")
            if username_exist:
                query = f""" SELECT u.user_id,
                                    u.username,
                                    u.password,
                                    ud.firstname,
                                    ud.lastname,
                                    ud.email,
                                    ud.phone,
                                    ud.joining_date,
                                    ud.profile_pic,
                                    ud.org_id,
                                    ud.designation,
                                    dl.domain_value AS  user_role
                                FROM user u 
                                INNER JOIN user_details ud ON u.user_id=ud.user_id
                                INNER JOIN domain_lookup dl ON dl.domain_code = ud.user_role
                                WHERE u.username='{username}' AND dl.domain_type='user_type'; 
                        """
                # logger.info(f"query:{query}")
                if query is not None:
                    cursor = connection.cursor()
                    cursor.execute(query)
                    cols = [col[0] for col in cursor.description] 
                    user_value = [dict(zip(cols,row)) for row in cursor.fetchall()]
                    user_md5_password = user_value[0]['password']
                    user_id = user_value[0]['user_id']
                    user_name = user_value[0]['firstname']+user_value[0]['lastname']
                    user_phone = user_value[0]['phone']
                    user_email = user_value[0]['email']
                    user_role = user_value[0]['user_role']
                    joining_date = user_value[0]['joining_date']
                    profile_pic = user_value[0]['profile_pic']
                    designation = user_value[0]['designation']
                    org_id = user_value[0]['org_id']
                    
                    
                input_md5_password = getMd5Hash(password)
                
                if input_md5_password is None:
                    raise OperationalException("Failed To Generate MD5 Hash")
                
                if str(input_md5_password) != str(user_md5_password):
                    raise InvalidCredentialException("Password not matched")
                
                logger.info("Password Matched Successfully")
                refresh = RefreshToken.for_user(User.objects.get(user_id=user_id))
                access_token = str(refresh.access_token)
                
                user_info = {"id":user_id, "name": user_name,"username":username ,"phone":user_phone,"email":user_email,'user_role':user_role,"org_id":org_id, "profile_pic":profile_pic,"joining_date":joining_date,"designation":designation, "access_token": access_token,"refresh_token": str(refresh)}
                
                response_body= {
                    'status': SUCCESSSTATUS,
                    'success': "true",
                    'message': "Record found.",
                    'data': user_info
                }
                
                return Response(response_body)
            else:
                raise UserNotExistsException("User Doesn't Exists")
            
    
    except MandatoryInputMissingException as mime:
        logger.exception(mime)
        ec.append(BE001)
        ec.append(BE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})    
    
    except UserNotExistsException as une:
        logger.exception(une)
        ec.append(IN002)
        ec.append(IN002MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[0].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
    except InvalidCredentialException as ice:
        logger.exception(ice)
        ec.append(BE005)
        ec.append(BE005MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[0].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
        
    except Exception as e:
        logger.exception(e)
        ec.append(SE001)
        ec.append(SE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[3].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
@api_view(['POST'])
def userView(request):
    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []
    logger.info("<======================== Start - User List ========================>")
    try:
        data = request.data
        logger.info(f"Requested Data = {data}")
        user_id  = data['user_id'] if data.get('user_id') else None
        
        if user_id  in ('' ,None):
            raise MandatoryInputMissingException("User Id Missing")
        else:
            user_id_exist = User.objects.filter(user_id=user_id,active=1).exists()
            if user_id_exist:
                user_details = UserDetails.objects.filter(user_id=user_id).first()
                user_role = DomainLookup.objects.filter(domain_code=user_details.user_role, domain_type='user_type').first()
                user_info = {
                        "user_id": user_details.user_id,
                        "firstname": user_details.firstname,
                        "lastname": user_details.lastname,
                        "email": user_details.email, 
                        "phone": user_details.phone,
                        "user_role": user_role.domain_value,
                        "profile_pic": user_details.profile_pic,
                        "designation": user_details.designation,
                        "salary": user_details.salary,
                        "joining_date": user_details.joining_date,
                        "created_on": user_details.created_on,
                        "updated_on": user_details.updated_on
                    }
                logger.info("User details fetched successfully")
                response_body= {
                    'status': SUCCESSSTATUS,
                    'success': "true",
                    'message': "Record found.",
                    'data': user_info
                }
                return Response(response_body)
            else:
                raise UserNotExistsException("User Doesn't Exists")
    except MandatoryInputMissingException as mime:
        logger.exception(mime)
        ec.append(BE001)
        ec.append(BE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
     
    except UserNotExistsException as une:
        logger.exception(une)
        ec.append(IN002)
        ec.append(IN002MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[0].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))}) 
      
    except UserNotAuthorized as una:
        logger.exception(una)
        ec.append(IN003)
        ec.append(IN003MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[0].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})   
        
    except Exception as e:
        logger.exception(e)
        ec.append(SE001)
        ec.append(SE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[3].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
    
@api_view(['POST'])
def userList(request):
    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []
    logger.info("<======================== Start - User List ========================>")
    try:
        data = request.data
        logger.info(f"Requested Data = {data}")
        user_id = data.get('user_id')
        org_id = data.get('org_id')
        
        if user_id in (None, ''):
            raise MandatoryInputMissingException("User Id Missing")
        if org_id in (None, ''):
            raise MandatoryInputMissingException("Organization Id Missing")
        
        user_id_exist = User.objects.filter(user_id=user_id, active=1).exists()
        if user_id_exist:
            user_details = UserDetails.objects.filter(user_id=user_id).first()
            if user_details:
                user_role = user_details.user_role
                if user_role not in (1, 2): 
                    raise UserNotAuthorized("User not authorized to perform this action")
                
                users_in_org = UserDetails.objects.filter(org_id=org_id)
                serialized_users = UserDetailsSerializer(users_in_org, many=True).data
                logger.info("User list fetched successfully")
                response_body= {
                'status': SUCCESSSTATUS,
                'success': "true",
                'message': "Record found.",
                'data': serialized_users
                }
                return Response(response_body)
            else:
                raise UserNotExistsException("User doesn't exist")
        else:
            raise UserNotExistsException("User doesn't exist")
    
    except MandatoryInputMissingException as mime:
        logger.exception(mime)
        ec.append("BE001")
        ec.append("Mandatory input missing")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[1].append(dict(zip(ek, ec)))
        return Response({ERROR: dict(zip(errorkeys, errordisplay))})
     
    except UserNotExistsException as une:
        logger.exception(une)
        ec.append("IN002")
        ec.append("User doesn't exist")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[0].append(dict(zip(ek, ec)))
        return Response({ERROR: dict(zip(errorkeys, errordisplay))}) 
      
    except UserNotAuthorized as una:
        logger.exception(una)
        ec.append("IN003")
        ec.append("User not authorized to perform this action")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[0].append(dict(zip(ek, ec)))
        return Response({ERROR: dict(zip(errorkeys, errordisplay))})   
        
    except Exception as e:
        logger.exception(e)
        ec.append("SE001")
        ec.append("An unexpected error occurred")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[3].append(dict(zip(ek, ec)))
        return Response({ERROR: dict(zip(errorkeys, errordisplay))})
    


@api_view(['POST'])
def userDelete(request):
    errorkeys = ['Info', 'Business_Errors', 'Warnings', 'System_Errors']
    errordisplay = [[], [], [], []]
    ec = []
    ek = []
    logger.info("<======================== Start - User Delete========================>")
    
    try:
        data = request.data
        logger.info(f"Requested Data = {data}")
        user_id = data.get('user_id')
        # org_id = data.get('org_id')
        user_id_to_delete = data.get('user_id_to_delete')
        
        if user_id in (None, ''):
            raise MandatoryInputMissingException("User Id Missing")
        # if org_id in (None, ''):
        #     raise MandatoryInputMissingException("Organization Id Missing")
        if user_id_to_delete in (None, ''):
            raise MandatoryInputMissingException("User id to delete is missing")
        
        user_org_id = UserDetails.objects.filter(user_id=user_id).values_list('org_id', flat=True).first()
        user_to_delete_org_id = UserDetails.objects.filter(user_id=user_id_to_delete).values_list('org_id', flat=True).first()
        
        if user_org_id != user_to_delete_org_id:
            raise UserNotAuthorized("Users do not belong to the same organization")
        
        # Check if user_id exists and has sufficient permissions
        user_id_exist = User.objects.filter(user_id=user_id, active=1).exists()
        if not user_id_exist:
            raise UserNotExistsException("User doesn't exist or is inactive")
        
        user_details = UserDetails.objects.filter(user_id=user_id).first()
        if not user_details:
            raise UserNotExistsException("User details not found")
        
        user_role = user_details.user_role
        if user_role not in (1, 2): 
            raise UserNotAuthorized("User not authorized to perform this action")
        
        user_id_to_delete_exist = User.objects.filter(user_id=user_id_to_delete, active=1).exists()
        if not user_id_to_delete_exist:
            raise UserNotExistsException("User to be deleted doesn't exist or is inactive")
        
        user_data = {
            "active": 0,
            "updated_on": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        User.objects.filter(user_id=user_id_to_delete).update(**user_data)
        logger.info("User deleted successfully")
        
        response_body = {
            'status': 'success',
            'success': True,
            'message': 'User deleted successfully.'
        }
        return Response(response_body)
    
    except MandatoryInputMissingException as mime:
        logger.exception(mime)
        ec.append("BE001")
        ec.append("Mandatory input missing")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[1].append(dict(zip(ek, ec)))
        return Response({'ERROR': dict(zip(errorkeys, errordisplay))})
     
    except UserNotExistsException as une:
        logger.exception(une)
        ec.append("IN002")
        ec.append("User doesn't exist or is inactive")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[0].append(dict(zip(ek, ec)))
        return Response({'ERROR': dict(zip(errorkeys, errordisplay))})
      
    except UserNotAuthorized as una:
        logger.exception(una)
        ec.append("IN003")
        ec.append("User not authorized to perform this action")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[0].append(dict(zip(ek, ec)))
        return Response({'ERROR': dict(zip(errorkeys, errordisplay))})
        
    except Exception as e:
        logger.exception(e)
        ec.append("SE001")
        ec.append("An unexpected error occurred")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[3].append(dict(zip(ek, ec)))
        return Response({'ERROR': dict(zip(errorkeys, errordisplay))})


@api_view(['POST'])
def createPost(request):
    errorkeys = ['Info', 'Business_Errors', 'Warnings', 'System_Errors']
    errordisplay = [[], [], [], []]
    ec = []
    ek = []
    logger.info("<======================== Start - Post Create========================>")
    try:
        data = request.data
        logger.info(f"data-{data}")
        user_id = data.get('user_id')
        user_id_exist = User.objects.filter(user_id=user_id, active=1).exists()
        
        if user_id_exist:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                post = serializer.save()
                response_body ={
                    'status': SUCCESSSTATUS,
                    'success': "true",
                    'data': PostSerializer(post).data
                }
                return Response(response_body)
            else:
                error_response = {}
                for field, errors in serializer.errors.items():
                    error_response[field] = errors[0]
                ec.append("BE001")
                ec.append("Invalid request data")
                ek.append("CODE")
                ek.append("MESSAGE")
                errordisplay[1].append(dict(zip(ek, ec)))
                errordisplay[1].append(error_response)
                return Response({ERROR: dict(zip(errorkeys, errordisplay))})
        else:
            raise UserNotExistsException("User doesn't exist")
    except UserNotExistsException as une:
        logger.exception(une)
        ec.append("IN002")
        ec.append("User doesn't exist")
        ek.append("CODE")
        ek.append("MESSAGE")
        errordisplay[0].append(dict(zip(ek, ec)))
        return Response({ERROR: dict(zip(errorkeys, errordisplay))})
            
    except Exception as e:
        logger.exception(e)
        ec.append(SE001)
        ec.append(SE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[3].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
        
    
    
