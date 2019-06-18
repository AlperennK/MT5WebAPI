from api import MyListener
from api import Credentials1
from api import Connection
from api import Client
from api import MT5Helper
import pytest
import os
import json
import time
import stomp


class Test_MT5_NEW_ACCOUNT(object):
    @pytest.fixture(scope='class')
    def amqcon(self):
        print("--------Test Setup---------")
        with pytest.allure.step('Connecting to Active MQ :'):
            host = Credentials1['ACTIVEMQ_IP']
            port = os.getenv("ACTIVEMQ_PORT") or 61613
            user = os.getenv("ACTIVEMQ_USER") or "smx"
            password = os.getenv("ACTIVEMQ_PASSWORD") or "smx"

            conn = stomp.Connection(host_and_ports=[(host, port)])
            lst = MyListener(conn)
            conn.set_listener('', lst)
            conn.start()
            conn.connect(login=user, passcode=password)
            conn.subscribe(destination='/topic/VirtualTopic.MT5.events', id=1, ack='auto')

        with pytest.allure.step('Generating new account :'):
            apicon=MT5Helper()
            lognum=apicon.add_user()['answer']['Login']
            print('New account number generated for this test : ', lognum)

        with pytest.allure.step('Filtering out non ping message headers and body : '):
            time.sleep(Credentials1['SLEEP'])
            headers = lst.hdr_list
            messages = lst.msg_list
            #apicon.del_user(lognum)
            converted=[json.loads(message.replace("'", "\"")) for message in messages if 'EventTimeStamp' in message]


        yield [[header for header in headers if header['MESSAGE_TYPE'] == 'ENTITY_EVENT' if header['ENTITY_ACTION'] == 'MT5_NEW_ACCOUNT'], [message for message in converted if int(lognum) == message['MT5Account']['Login']], lognum]
        print("----Test tear down----------")

###HEADERS###

    def test_Account_Type_DataType(self,amqcon):
        "ACCOUNT TYPE / JIRA CASE MT-779 / Account Type DataType"
        print(amqcon[0])
        account_type=[message['ACCOUNT_TYPE'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in account_type)

    def test_Account_Type_Value(self,amqcon):
        "Account Type / JIRA CASE MT-815 / Account Type Value"
        print(amqcon[0])
        account_type=[message['ACCOUNT_TYPE'] for message in amqcon[0]]
        assert 'MT5_MARKET' in account_type


    def test_Message_Type_DataType(self,amqcon):
        "Message Type / JIRA CASE MT-795 / Message Type"
        print(amqcon[0])
        message_type= [message['MESSAGE_TYPE'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in message_type)

    def test_Message_Type_Mandatory(self,amqcon):
        "Message Type / JIRA CASE MT-806 / Message Type"
        print(amqcon[0])
        message_type= [message['MESSAGE_TYPE'] for message in amqcon[0]]
        assert [] != message_type

    def test_Message_Type_Parameter_Value(self,amqcon):
        "Message Type / JIRA CASE MT-T831 (1.0)"
        print(amqcon[0])
        message_type= [message['MESSAGE_TYPE'] for message in amqcon[0]]
        assert 'ENTITY_EVENT' in message_type


    def test_Entity_Type_DataType(self,amqcon):
        "ENTITY TYPE / JIRA CASE MT-785 / ENTITY TYPE DataType"
        print(amqcon[0])
        message_entity= [message['ENTITY_TYPE'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in message_entity)

#Hardcoded with message reference
    def test_Entity_Type_Value(self,amqcon):
        "ENTITY TYPE / JIRA CASE MT-841 / ENTITY TYPE Value"
        print(amqcon[0])
        message_entity= [message['ENTITY_TYPE'] for message in amqcon[0]]
        assert 'client' in message_entity

    def test_Entity_Type_Mandatory(self,amqcon):
        "ENTITY TYPE / JIRA CASE MT-842 / ENTITY TYPE Mandatory"
        print(amqcon[0])
        message_entity= [message['ENTITY_TYPE'] for message in amqcon[0]]
        assert [] != message_entity


    def test_Entity_Action_DataType(self,amqcon):
        "Entity Status / JIRA CASE MT-783 / ENTITY STATUS DataType"
        print(amqcon[0])
        message_entity_action =[message['ENTITY_ACTION'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in message_entity_action)


    def test_Entity_Action_Value(self,amqcon):
        "#Entity Action / JIRA CASE MT-820 (v2.0) / ENTITY STATUS Value"
        print(amqcon[0])
        message_entity_action =[message['ENTITY_ACTION'] for message in amqcon[0]]
        assert 'MT5_NEW_ACCOUNT' in message_entity_action

    def test_Message_Producer_Instance_DataType(self,amqcon):
        "Message Producer DataType/ JIRA CASE MT-T794 / DataType Field MESSAGE_PRODUCER"
        print(amqcon[0])
        message_producer=[message['MESSAGE_PRODUCER_INSTANCE'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in message_producer)

#Hardcoded to value 'MTEventTransmitter'
    def test_Message_Producer_Instance_Value(self,amqcon):
        "Message Producer DataType/ JIRA CASE MT-T830 / DataType Field MESSAGE_PRODUCER"
        print(amqcon[0])
        message_producer=[message['MESSAGE_PRODUCER_INSTANCE'] for message in amqcon[0]]
        assert 'MT5_REAL' in message_producer

    def test_Message_Producer_Instance_Mandatory(self,amqcon):
        "Message Producer DataType/ JIRA CASE MT-T844 / DataType Field MESSAGE_PRODUCER"
        print(amqcon[0])
        message_producer=[message['MESSAGE_PRODUCER_INSTANCE'] for message in amqcon[0]]
        assert 'MT5_REAL' in message_producer

    def test_Message_Created_DataType(self,amqcon):
        "Message Created DataType/ JIRA CASE MT-T770 / DataType Field MESSAGE_CREATED"
        print(amqcon[0])
        message_created=[message['MESSAGE_CREATED'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in message_created)

    def test_Message_Created_Mandatory(self,amqcon):
        "Message Created DataType/ JIRA CASE MT-T803 / DataType Field MESSAGE_CREATED"
        print(amqcon[0])
        message_created=[message['MESSAGE_CREATED'] for message in amqcon[0]]
        assert [] != message_created


    def test_Message_Format_DataType(self,amqcon):
        "#Message Format Datatype / JIRA CASE MT-T792 (1.0)"
        print(amqcon[0])
        message_format = [message['MESSAGE_FORMAT'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in message_format)

    def test_Message_Format_Mandatory(self,amqcon):
        "#Message Format Mandatory / JIRA CASE MT-T804 (1.0)"
        print(amqcon[0])
        message_format = [message['MESSAGE_FORMAT'] for message in amqcon[0]]
        assert [] != message_format

    def test_Message_Format_Value(self,amqcon):
        "#Message Format Datatype / JIRA CASE MT-T828 (1.0)"
        print(amqcon[0])
        message_format = [message['MESSAGE_FORMAT'] for message in amqcon[0]]
        assert 'v1' in message_format



    def test_Message_Producer_DataType(self,amqcon):
        "Message Producer DataType/ JIRA CASE MT-T792 / DataType Field MESSAGE_PRODUCER"
        print(amqcon[0])
        message_producer=[message['MESSAGE_PRODUCER'] for message in amqcon[0]]
        assert all(isinstance(item, str) for item in message_producer)

    def test_Message_Producer_Mandatory(self,amqcon):
        "Message Producer DataType/ JIRA CASE MT-T792 / DataType Field MESSAGE_PRODUCER"
        print(amqcon[0])
        message_producer=[message['MESSAGE_PRODUCER'] for message in amqcon[0]]
        assert [] != message_producer

    def test_Message_Producer_Value(self,amqcon):
        "Message Producer Instance Value/ JIRA CASE MT-T828 / Value of MESSAGE_PRODUCER"
        print(amqcon[0])
        message_producer=[message['MESSAGE_PRODUCER'] for message in amqcon[0]]
        assert 'MTEventTransmitter' in message_producer

### Message Body ###

    def test_ID_DataType(self, amqcon):
        "ID / JIRA CASE MT-788/ ID Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        id=[message['MT5Account']['ID'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in id)

    def test_ID_Value(self, amqcon):
        "ID / JIRA CASE MT-824/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        id=[message['MT5Account']['ID'] for message in amqcon[1]]
        assert '' == id[0]

    def test_ID_Mandatory(self, amqcon):
        "ID / JIRA CASE MT-845/ ID Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        id=[message['MT5Account']['ID'] for message in amqcon[1]]
        assert [] != id[0]


    def test_City_DataType(self, amqcon):
        "ID / JIRA CASE MT-846/ ID Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        city=[message['MT5Account']['City'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in city)


    def test_City_Mandatory(self, amqcon):
        "ID / JIRA CASE MT-848/ ID Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        city=[message['MT5Account']['City'] for message in amqcon[1]]
        assert [] != city


    def test_City_Value(self, amqcon):
        "ID / JIRA CASE MT-847/ ID Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        city=[message['MT5Account']['City'] for message in amqcon[1]]
        assert 'Podgorica' in city



    def test_MQID_DataType(self, amqcon):
        "ID / JIRA CASE MT-796/ ID Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        id=[message['MT5Account']['MQID'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in id)

    def test_MQID_Value(self, amqcon):
        "ID / JIRA CASE MT-832/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        mqid=[message['MT5Account']['MQID'] for message in amqcon[1]]
        assert "E58970C" in mqid

    def test_MQID_Mandatory(self, amqcon):
        "ID / JIRA CASE MT-845/ ID Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        mqid=[message['MT5Account']['MQID'] for message in amqcon[1]]
        assert [] != mqid[0]

    def test_Name_DataType(self, amqcon):
        "ID / JIRA CASE MT-851/ ID DataType "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        name=[message['MT5Account']['Name'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in name)


    def test_Name_Mandatory(self, amqcon):
        "ID / JIRA CASE MT-852/ ID Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        name=[message['MT5Account']['Name'] for message in amqcon[1]]
        assert [] != name[0]


    def test_Name_Value(self, amqcon):
        "ID / JIRA CASE MT-850/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        name=[message['MT5Account']['Name'] for message in amqcon[1]]
        assert "testertest" == name[0]


    def test_Agent_Datatype(self, amqcon):
        "ID / JIRA CASE MT-853/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        agent=[message['MT5Account']['Agent'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in agent)

    def test_Agent_Mandatory(self, amqcon):
        "ID / JIRA CASE MT-854/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        agent=[message['MT5Account']['Agent'] for message in amqcon[1]]
        assert [] != agent[0]


    def test_Agent_Value(self, amqcon):
        "ID / JIRA CASE MT-855/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        agent=[message['MT5Account']['Agent'] for message in amqcon[1]]
        assert 0 == agent[0]

    def test_Color_Datatype(self, amqcon):
        "Color / JIRA CASE MT-856/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        color=[message['MT5Account']['Color'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in color)

    def test_Color_Mandatory(self, amqcon):
        "Color / JIRA CASE MT-857/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        color=[message['MT5Account']['Color'] for message in amqcon[1]]
        assert [] != color

    def test_Color_Value(self, amqcon):
        "Color / JIRA CASE MT-858/ ID Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        color=[message['MT5Account']['Color'] for message in amqcon[1]]
        assert 4278190080 in color

    def test_Email_Datatype(self, amqcon):
        "Email / JIRA CASE MT-859/ Email Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        email=[message['MT5Account']['Email'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in email)


    def test_Email_Mandatory(self, amqcon):
        "Email / JIRA CASE MT-860/ Email Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        email=[message['MT5Account']['Email'] for message in amqcon[1]]
        assert [] != email


    def test_Email_Value(self, amqcon):
        "Email / JIRA CASE MT-861/ Email Value"
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        email=[message['MT5Account']['Email'] for message in amqcon[1]]
        assert "" in email

    def test_Group_Datatype(self, amqcon):
        "Group / JIRA CASE MT-774/ Group Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        group=[message['MT5Account']['Group'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in group)


    def test_Group_Mandatory(self, amqcon):
        "Group / JIRA CASE MT-812/ Group Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        group=[message['MT5Account']['Group'] for message in amqcon[1]]
        assert [] != group

    def test_Group_Value(self, amqcon):
        "Group / JIRA CASE MT-823/ Group Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        group=[message['MT5Account']['Group'] for message in amqcon[1]]
        assert "market-en" in group

    def test_Login_Datatype(self, amqcon):
        "Login / JIRA CASE MT-790/ Login Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        login=[message['MT5Account']['Login'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in login)


    def test_Login_Mandatory(self, amqcon):
        "Login / JIRA CASE MT-802/ Login Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        login=[message['MT5Account']['Login'] for message in amqcon[1]]
        assert [] != login


    def test_Login_Value(self, amqcon):
        "login / JIRA CASE MT-827/ Login Value"
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        login=[message['MT5Account']['Login'] for message in amqcon[1]]
        assert int(amqcon[2]) in login


    def test_Phone_Datatype(self, amqcon):
        "Phone / JIRA CASE MT-862/ Phone Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        phone=[message['MT5Account']['Phone'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in phone)


    def test_Phone_Mandatory(self, amqcon):
        "Phone / JIRA CASE MT-863/ Phone Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        phone=[message['MT5Account']['Phone'] for message in amqcon[1]]
        assert [] != phone


    def test_Phone_Value(self, amqcon):
        "Phone / JIRA CASE MT-864/ Phone Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        phone=[message['MT5Account']['Phone'] for message in amqcon[1]]
        assert "" in  phone

    def test_State_Datatype(self, amqcon):
        "State / JIRA CASE MT-865/ State Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        state=[message['MT5Account']['State'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in state)

    def test_State_Mandatory(self, amqcon):
        "State / JIRA CASE MT-866/ State Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        state=[message['MT5Account']['State'] for message in amqcon[1]]
        assert [] != state

    def test_State_Value(self, amqcon):
        "State / JIRA CASE MT-867/ State Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        state=[message['MT5Account']['State'] for message in amqcon[1]]
        assert "" in state

    def test_Credit_Datatype(self, amqcon):
        "Credit / JIRA CASE MT-868/ Credit Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        credit=[message['MT5Account']['Credit'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in credit)

    def test_Credit_Mandatory(self, amqcon):
        "Credit / JIRA CASE MT-869/ Credit Mnadatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        credit=[message['MT5Account']['Credit'] for message in amqcon[1]]
        assert [] != credit

    def test_Credit_Value(self, amqcon):
        "Credit / JIRA CASE MT-870/ Credit Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        credit=[message['MT5Account']['Credit'] for message in amqcon[1]]
        assert 0 in credit

    def test_Margin_Datatype(self, amqcon):
        "Margin / JIRA CASE MT-871/ Margin Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        margin=[message['MT5Account']['Margin'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in margin)


    def test_Margin_Mandatory(self, amqcon):
        "Margin / JIRA CASE MT-872/ Margin Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        margin=[message['MT5Account']['Margin'] for message in amqcon[1]]
        assert [] != margin


    def test_Margin_Value(self, amqcon):
        "Margin / JIRA CASE MT-873/ Margin Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        margin=[message['MT5Account']['Margin'] for message in amqcon[1]]
        assert 0 in margin

    def test_Rights_Datatype(self, amqcon):
        "Rights / JIRA CASE MT-874/ Rights Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        rights=[message['MT5Account']['Rights'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in rights)


    def test_Rights_Mandatory(self, amqcon):
        "Rights / JIRA CASE MT-875/ Rights Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        rights=[message['MT5Account']['Rights'] for message in amqcon[1]]
        assert [] != rights

    def test_Rights_Value(self, amqcon):
        "Rights / JIRA CASE MT-876/ Rights Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        rights=[message['MT5Account']['Rights'] for message in amqcon[1]]
        assert 2531 in rights

    def test_Status_Datatype(self, amqcon):
        "Status / JIRA CASE MT-877/ Status Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        status=[message['MT5Account']['Status'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in status)

    def test_Status_Mandatory(self, amqcon):
        "Status / JIRA CASE MT-878/ Status Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        status=[message['MT5Account']['Status'] for message in amqcon[1]]
        assert [] != status

    def test_Status_Value(self, amqcon):
        "Status / JIRA CASE MT-879/ Status Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        status=[message['MT5Account']['Status'] for message in amqcon[1]]
        assert "" in status


    def test_Account_DataType(self, amqcon):
        "Status / JIRA CASE MT-880/ Status Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        account=[message['MT5Account']['Account'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in account)



    def test_Account_Mandatory(self, amqcon):
        "Status / JIRA CASE MT-881/ Status Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        account=[message['MT5Account']['Account'] for message in amqcon[1]]
        assert [] != account


    def test_Account_Value(self, amqcon):
        "Status / JIRA CASE MT-882/ Status Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        account=[message['MT5Account']['Account'] for message in amqcon[1]]
        assert "" in account


    def test_Balance_DataType(self, amqcon):
        "balance / JIRA CASE MT-883/ balance Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balance=[message['MT5Account']['Balance'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in balance)


    def test_Balance_Mandatory(self, amqcon):
        "balance / JIRA CASE MT-884/ balance Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balance=[message['MT5Account']['Balance'] for message in amqcon[1]]
        assert [] != balance


    def test_Balance_Value(self, amqcon):
        "balance / JIRA CASE MT-885/ balance Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balance=[message['MT5Account']['Balance'] for message in amqcon[1]]
        assert 0 in balance


    def test_Comment_DataType(self, amqcon):
        "Comment / JIRA CASE MT-772/ Comment Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        comment=[message['MT5Account']['Comment'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in comment)



    def test_Comment_Mandatory(self, amqcon):
        "Comment / JIRA CASE MT-808/ Comment Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        comment=[message['MT5Account']['Comment'] for message in amqcon[1]]
        assert [] != comment


    def test_Comment_Value(self, amqcon):
        "Comment / JIRA CASE MT-836/ Comment Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        comment=[message['MT5Account']['Comment'] for message in amqcon[1]]
        assert "" in comment

    def test_Company_DataType(self, amqcon):
        "Company / JIRA CASE MT-886/ balance Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        company=[message['MT5Account']['Company'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in company)



    def test_Company_Mandatory(self, amqcon):
        "Company / JIRA CASE MT-887/ balance Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        company=[message['MT5Account']['Company'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in company)

    def test_Company_Value(self, amqcon):
        "Company / JIRA CASE MT-888/ Company Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        company=[message['MT5Account']['Company'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in company)

    def test_ZipCode_DataType(self, amqcon):
        "ZipCode / JIRA CASE MT-889/ ZipCode Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        zipCode=[message['MT5Account']['ZipCode'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in zipCode)

    def test_ZipCode_Mandatory(self, amqcon):
        "ZipCode / JIRA CASE MT-890/ ZipCode Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        zipCode=[message['MT5Account']['ZipCode'] for message in amqcon[1]]
        assert [] != zipCode

    def test_ZipCode_Value(self, amqcon):
        "ZipCode / JIRA CASE MT-891/ ZipCode Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        zipCode=[message['MT5Account']['ZipCode'] for message in amqcon[1]]
        assert "" in zipCode

    def test_Language_DataType(self, amqcon):
        "Language / JIRA CASE MT-892/ Language Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        language=[message['MT5Account']['Language'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in language)

    def test_Language_Mandaroty(self, amqcon):
        "Language / JIRA CASE MT-893/ Language Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        language=[message['MT5Account']['Language'] for message in amqcon[1]]
        assert [] != language

    def test_Language_Value(self, amqcon):
        "Language / JIRA CASE MT-894/ Language Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        langauge=[message['MT5Account']['Language'] for message in amqcon[1]]
        assert 0 in langauge

    def test_Leverage_DataType(self, amqcon):
        "Leverage / JIRA CASE MT-895/ Language Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        leverage=[message['MT5Account']['Leverage'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in leverage)

    def test_Leverage_Mandatory(self, amqcon):
        "Leverage / JIRA CASE MT-896/ Language Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        leverage=[message['MT5Account']['Leverage'] for message in amqcon[1]]
        assert [] != leverage

    def test_Leverage_Value(self, amqcon):
        "Leverage / JIRA CASE MT-897/ Language Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        leverage=[message['MT5Account']['Leverage'] for message in amqcon[1]]
        assert 100 in leverage

    def test_LastAccess_DataType(self, amqcon):
        "LastAccess / JIRA CASE MT-898/ LastAccess Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        lastaccess=[message['MT5Account']['LastAccess'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in lastaccess)


    def test_LastAccess_Mandatory(self, amqcon):
        "LastAccess / JIRA CASE MT-899/ LastAccess Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        lastaccess=[message['MT5Account']['LastAccess'] for message in amqcon[1]]
        assert [] != lastaccess

#Check db and compare
    def test_LastAccess_Value(self, amqcon):
        "LastAccess / JIRA CASE MT-900/ LastAccess Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        lastaccess=[message['MT5Account']['LastAccess'] for message in amqcon[1]]
        pass


    def test_LeadSource_Datatype(self, amqcon):
        "LeadSource / JIRA CASE MT-901/ LeadSource Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        leadSource=[message['MT5Account']['LeadSource'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in leadSource)

    def test_LeadSource_Mandatory(self, amqcon):
        "LeadSource / JIRA CASE MT-902/ LeadSource Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        leadSource=[message['MT5Account']['LeadSource'] for message in amqcon[1]]
        assert [] != leadSource

    def test_LeadSource_Value(self, amqcon):
        "LeadSource / JIRA CASE MT-903/ LeadSource Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        leadSource=[message['MT5Account']['LeadSource'] for message in amqcon[1]]
        assert "" in leadSource

    def test_CurrencyCode_Datatype(self, amqcon):
        "CurrencyCode / JIRA CASE MT-773/ CurrencyCode Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        currencyCode=[message['MT5Account']['CurrencyCode'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in currencyCode)

    def test_CurrencyCode_Mandatory(self, amqcon):
        "CurrencyCode / JIRA CASE MT-810/ CurrencyCode Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        currencyCode=[message['MT5Account']['CurrencyCode'] for message in amqcon[1]]
        assert [] != currencyCode

    def test_CurrencyCode_Value(self, amqcon):
        "CurrencyCode / JIRA CASE MT-838/ CurrencyCode Value"
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        currencyCode=[message['MT5Account']['CurrencyCode'] for message in amqcon[1]]
        assert 'USD' in currencyCode

    def test_InterestRate_Datatype(self, amqcon):
        "InterestRate / JIRA CASE MT-904/ InterestRate Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        interestRate=[message['MT5Account']['InterestRate'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in interestRate)

    def test_InterestRate_Mandatory(self, amqcon):
        "InterestRate / JIRA CASE MT-905/ InterestRate Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        interestRate=[message['MT5Account']['InterestRate'] for message in amqcon[1]]
        assert [] != interestRate


    def test_InterestRate_Value(self, amqcon):
        "InterestRate / JIRA CASE MT-906/ InterestRate Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        interestRate=[message['MT5Account']['InterestRate'] for message in amqcon[1]]
        assert 0 in interestRate

    def test_Registration_DataType(self, amqcon):
        "Registration / JIRA CASE MT-907/ Registration Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        registration=[message['MT5Account']['Registration'] for message in amqcon[1]]
        assert all(isinstance(item, str) for item in registration)

    def test_Registration_Mandatory(self, amqcon):
        "Registration / JIRA CASE MT-908/ Registration Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        registration=[message['MT5Account']['Registration'] for message in amqcon[1]]
        assert [] != registration

#Pull from DB.
    def test_Registration_Value(self, amqcon):
        "Registration / JIRA CASE MT-909/ Registration Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        with pytest.allure.step('Getting Registration Field  :'):
            registration=[message['MT5Account']['Registration'] for message in amqcon[1]]
        with pytest.allure.step('Getting registration time from db : '):
            registration_db=Client().check_login(amqcon[2])['Registration'].strftime("%Y-%m-%d %H:%M:%S")
        with pytest.allure.step('Comparing values : '):
            assert registration_db in registration


    def test_EquityPrevDay_DataType(self, amqcon):
        "equityPrevDay / JIRA CASE MT-910/ equityPrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        equityPrevDay=[message['MT5Account']['EquityPrevDay'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in equityPrevDay)

    def test_EquityPrevDay_Mandatory(self, amqcon):
        "equityPrevDay / JIRA CASE MT-911/ equityPrevDay Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        equityPrevDay=[message['MT5Account']['EquityPrevDay'] for message in amqcon[1]]
        assert [] != equityPrevDay


    def test_EquityPrevDay_Value(self, amqcon):
        "equityPrevDay / JIRA CASE MT-912/ equityPrevDay Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        equityPrevDay=[message['MT5Account']['EquityPrevDay'] for message in amqcon[1]]
        assert 0 in equityPrevDay

    def test_BalancePrevDay_DataType(self, amqcon):
        "balancePrevDay / JIRA CASE MT-913/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balancePrevDay=[message['MT5Account']['BalancePrevDay'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in balancePrevDay)


    def test_BalancePrevDay_Mandatory(self, amqcon):
        "balancePrevDay / JIRA CASE MT-914/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balancePrevDay=[message['MT5Account']['BalancePrevDay'] for message in amqcon[1]]
        assert [] != balancePrevDay


    def test_BalancePrevDay_Value(self, amqcon):
        "balancePrevDay / JIRA CASE MT-915/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balancePrevDay=[message['MT5Account']['BalancePrevDay'] for message in amqcon[1]]
        assert 0 in balancePrevDay

    def test_CommissionDaily_DataType(self, amqcon):
        "balancePrevDay / JIRA CASE MT-913/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        commissionDaily=[message['MT5Account']['BalancePrevDay'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in commissionDaily)

    def test_CommissionDaily_Mandatory(self, amqcon):
        "balancePrevDay / JIRA CASE MT-913/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        commissionDaily=[message['MT5Account']['BalancePrevDay'] for message in amqcon[1]]
        assert [] != commissionDaily


    def test_CommissionDaily_Value(self, amqcon):
        "balancePrevDay / JIRA CASE MT-913/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        commissionDaily=[message['MT5Account']['BalancePrevDay'] for message in amqcon[1]]
        assert 0 in commissionDaily

    def test_EquityPrevMonth_DataType(self, amqcon):
        "balancePrevDay / JIRA CASE MT-915/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        equityPrevMonth=[message['MT5Account']['EquityPrevMonth'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in equityPrevMonth)

    def test_EquityPrevMonth_Mandatory(self, amqcon):
        "balancePrevDay / JIRA CASE MT-915/ balancePrevDay Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        equityPrevMonth=[message['MT5Account']['EquityPrevMonth'] for message in amqcon[1]]
        assert [] != equityPrevMonth

    def test_EquityPrevMonth_Value(self, amqcon):
        "balancePrevDay / JIRA CASE MT-921/ balancePrevDay Value"
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        equityPrevMonth=[message['MT5Account']['BalancePrevMonth'] for message in amqcon[1]]
        assert 0 in equityPrevMonth

    def test_BalancePrevMonth_DataType(self, amqcon):
        "BalancePrevMonth / JIRA CASE MT-922/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balancePrevMonth=[message['MT5Account']['EquityPrevMonth'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in balancePrevMonth)

    def test_BalancePrevMonth_Mandatory(self, amqcon):
        "BalancePrevMonth / JIRA CASE MT-923/ balancePrevDay Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balancePrevMonth=[message['MT5Account']['BalancePrevMonth'] for message in amqcon[1]]
        assert [] != balancePrevMonth

    def test_BalancePrevMonth_Value(self, amqcon):
        "BalancePrevMonth / JIRA CASE MT-924/ balancePrevDay Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        balancePrevMonth=[message['MT5Account']['BalancePrevMonth'] for message in amqcon[1]]
        assert 0 in balancePrevMonth

    def test_CertSerialNumber_DataType(self, amqcon):
        "BalancePrevMonth / JIRA CASE MT-925/ balancePrevDay Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        certSerialNumber=[message['MT5Account']['EquityPrevMonth'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in certSerialNumber)

    def test_CertSerialNumber_Mandatory(self, amqcon):
        "certSerialNumber / JIRA CASE MT-926/ certSerialNumber Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        certSerialNumber=[message['MT5Account']['CertSerialNumber'] for message in amqcon[1]]
        assert [] != certSerialNumber

    def test_CertSerialNumber_Value(self, amqcon):
        "certSerialNumber / JIRA CASE MT-927/ certSerialNumber Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        certSerialNumber=[message['MT5Account']['CertSerialNumber'] for message in amqcon[1]]
        assert 0 in certSerialNumber

    def test_CommissionMonthly_DataType(self, amqcon):
        "commissionMonthly / JIRA CASE MT-928/ commissionMonthly Datatype "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        commissionMonthly=[message['MT5Account']['CommissionMonthly'] for message in amqcon[1]]
        assert all(isinstance(item, int) for item in commissionMonthly)

    def test_CommissionMonthly_Mandatory(self, amqcon):
        "commissionMonthly / JIRA CASE MT-929/ commissionMonthly Mandatory "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        commissionMonthly=[message['MT5Account']['CommissionMonthly'] for message in amqcon[1]]
        assert [] != commissionMonthly

    def test_CommissionMonthly_Value(self, amqcon):
        "commissionMonthly / JIRA CASE MT-930/ commissionMonthly Value "
        print("Message Body :", amqcon[1])
        print("Header :" , amqcon[0])
        commissionMonthly=[message['MT5Account']['CommissionMonthly'] for message in amqcon[1]]
        assert 0 in commissionMonthly
