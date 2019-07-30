'''
Created on Nov 17, 2016

@author: PDINDA

Expected Input:

{
   *************EXTRA NOT REQUIRED DETAILS*****************
   *********************************************************
    "steps_to_auth" : [
    {
            "username" : "asdsds",//
            "host" : "pdinda02",
            "password" : "asdsdsad",
            "type" : "telnet",
            "order" : 1
        },
          {
            "username" : "asdsds",//
            "host" : "pdinda02",
            "password" : "asdsdsad",
            "type" : "ssh",
            "order" : 2
        },
          {
            "username" : "asdsds",//
            "host" : "pdinda02",
            "password" : "asdsdsad",
            "type" : "ssh",
            "order" : 3
        }
    ],
    **************************************************************
    *************EXTRA NOT REQUIRED DETAILS*****************
}

'''
import logging,re,telnetlib,traceback

from autologging import logged
from fabric2 import connection


hosts_count = {}


@logged(logging.getLogger("RemoteAuthenticationService"))
class RemoteAuthenticationService():

    # Init's Data
    def __init__(self):
        #         self.func_options = {'ssh': self.ssh,
        #                              'telnet': self.telnet}

        self.key = "steps_to_auth"  # KET OF AUTH # SHOULD BE LIST AS GIVEN ABOVE
        self.default_port = str(22)

    def extract_time(self, json):
        """convert update_time string to int"""
        try:
            # Also convert to int since update_time will be string.  When comparing
            # strings, "10" is smaller than "2".
            return int(json['order'])
        except KeyError:
            return 0

    def callFinalMethod(self, step, fn, *args, **kwargs):
        """This Method Call Final Method With Argument or Without Argument"""
        fn(*args, **kwargs)

    def validateConnectionSettings(self, rec):
        """Start of validate Connection Settings"""
        # CHECK OUTHER AUTHORIZATION # PORT IS ADDED IF NOT PRESENT SO SKIP
        # CHECK
        if rec.get("username") is None:
            raise ValueError("username was not found in request")
        if rec.get("ip") is None:
            raise ValueError("ip was not found in request")
        if rec.get("host") is None:
            raise ValueError("host was not found in request")
        if rec.get("password") is None:
            raise ValueError("password was not found in request")

        # CHECK STEPS TO AUTH  # PORT IS ADDED IF NOT PRESENT SO SKIP CHECK
        if rec.get(self.key):
            for data in rec[self.key]:
                if data.get("username") is None:
                    raise ValueError("username was not found in request")
                if data.get("host") is None:
                    raise ValueError("host was not found in request")
                if data.get("password") is None:
                    raise ValueError("password was not found in request")

    def genareate_gateway_connection_object(self, machine):
        '''
         gen the gateway connection for fabric2

        :param machine:
        :return:
            final_gateway - fabric2 Connection object
        '''

        assert machine, "machine details are empty"

        gateway_object_list = []

        if machine.get(self.key):
            for data in machine[self.key]:
                if data["type"].lower() == "ssh":
                    if not data.get("port"):
                        # IF PORT NOT PRESENT ADD DEFAULT
                        data["port"] = self.default_port
                        print "##############################NOTE##############################"
                        print ' For GATEWAY SSH ' + data['host'] \
                              + ' no port was specified.Using default port as :' \
                              + self.default_port
                        print "##############################NOTE##############################"
                    # create gateway list
                    gateway_con = connection.Connection(
                        host=data["username"] + '@' +
                        data["host"] + ":" + str(data["port"]),
                        connect_kwargs={"password": data["password"]})
                    gateway_object_list.append(gateway_con)

            final_gateway = None

            if len(gateway_object_list) == 1:
                return gateway_object_list[0]

            if len(gateway_object_list) > 1:
                for i, gateway in enumerate(gateway_object_list):

                    if i > 0:
                        # set the previous connections has gateway
                        gateway.gateway = gateway_object_list[i - 1]
                        final_gateway = gateway

                return final_gateway
            else:
                return None
        else:
            return None
        
    def telnet(self, machine):
        '''
         gen the connection for telnet

        :param machine:
        :return:
            connection via telnet
        '''

        assert machine, "machine details are empty"

        
        if machine.get(self.key):
            for data in machine[self.key]:
                if data["type"].lower() == "telnet":
                    """Start of Telnet"""
                    try:
                        Username = data["username"]
                        Password = data["password"]
                        tn = telnetlib.Telnet(data["host"])
                        UNameresponse = tn.expect([re.compile(b"login:"), re.compile(
                            b"#"), re.compile(b":"), re.compile(b"username:")])
                        if UNameresponse[0] < 0:  # No match found
                            raise RuntimeError("Login prompt was not received")
                        tn.write(str(Username) + "\n")
                        Passwordresponse = tn.expect(
                            [re.compile(b":"), re.compile(b"password:")])
                        if Passwordresponse[0] < 0:  # No match found
                            raise RuntimeError("Login prompt was not received")
                        tn.write(str(Password) + "\n")
                    except Exception as e:
                        traceback.print_exc()
                        print 'Error while performing Telnet to :' \
                            + data['host'] + \
                            ' with error ' + str(e)
                    finally:
                        try:
                            tn.close()
                        except Exception as e:
                            print 'Error while closing Telnet to :' \
                                + data['host'] + \
                                ' with error :' + str(e)
                       
            

            
    # Authenticate to pull from machine
    # We are using reflection here
    # We only perform telnet once
    # With reflection we check steps_to_auth and perform reflection
    # From telnet we pull data
    def authenticate(self, machine, fn, *args, **kwargs):
        """Start of Authentication"""
        global hosts_count
        try:

            self.validateConnectionSettings(machine)

            # CHECK DATA
            if machine and len(machine) > 0 and machine.get(self.key) and len(machine.get(self.key)) > 0:
                machine[self.key].sort(key=self.extract_time, reverse=False)

            # ADD TARGET MACHINE DETAILS

            if not machine.get("port"):
                # IF PORT NOT PRESENT ADD DEFAULT
                machine["port"] = self.default_port
                print "##############################NOTE##############################"
                print ' For SSH to target machine: ' + machine['host'] \
                    + ' no port was specified.Using default port as:' \
                    + self.default_port
                print "##############################NOTE##############################"

            host = machine["username"] + '@' + \
                machine["host"] + ":" + str(machine["port"])
            host_password = machine["password"]

            # ADD GATEWAY
            final_gateway = self.genareate_gateway_connection_object(machine)

            # build the the final host connection with gateway
            assert host, 'host connection details is empty'
            assert host_password, 'host_password  is empty'

            if final_gateway:
                final_host = connection.Connection(host=host, connect_kwargs={
                                                   "password": host_password }, gateway=final_gateway)
            else:
                final_host = connection.Connection(host=host, connect_kwargs={
                                                   "password": host_password })
            try:
                with final_host as c:
                    kwargs['connect'] = c
                    kwargs['shell_type'] = machine.get("shell_type", None)
                    kwargs['reload_command'] = machine.get(
                        "reload_command", None)
                    self.telnet(machine) # PERFORM TELNET IF ANY
                    self.callFinalMethod(machine, fn, *args, **kwargs)
            except Exception as exp:
                raise exp

        except Exception as e:  # catch *all* exceptions
            raise e