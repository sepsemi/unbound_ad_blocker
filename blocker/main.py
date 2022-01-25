import re
import datetime
from blocker.database import Database

database = Database()
regex_paterns = []

class QueryValidator:
    def __init__(self, domain):
        self.tld = domain.split('.')[-1]
        self.lenght = len(domain)
        self.domain = domain


    def should_block(self):
        # Check multiple routs and return True or False
        # Check whitelist first
        if self.is_whitelisted():
            return False
        
        # Then we check the regex due to performance concerns
        if self.is_blacklisted_regex_match():
            self.log('regex')
            return True
        
        # This is the worst case scenario
        if self.is_blacklisted():
            self.log('database')
            return True
            
    def is_whitelisted(self):
        # All we really need is a result. 
        # if there is no result then there is nothing to blacklist
        return database.table_fetch_one('whitelist', tld=self.tld, lenght=self.lenght, domain=self.domain)
        
    def is_blacklisted_regex_match(self):
        # Loop though the compiled regex list.
        # and check for a match if nothing matches then there is nothing to blacklist.
        for patern in regex_paterns: 
            if patern.search(self.domain):
                return True
            
    def is_blacklisted(self):
        # Estenially the same as is_whitelisted
        # if there is no result then there is nothing to blacklist
        return database.table_fetch_one('blacklist', tld=self.tld,lenght=self.lenght, domain=self.domain)
    
    def log(self, _type):
        dt = datetime.datetime.now()
        log_info("[module][{}][QueryValidator][blocked][{}]: {}".format(dt, _type, self.domain))

def init(id, cfg):
    # Load the regex paterns
   
    with open('/usr/local/etc/unbound/blocker/etc/paterns.txt', 'r') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            regex_paterns.append(re.compile(r'{}'.format(line)))
     
    return True

def deinit(id):
    return True

def inform_super(id, qstate, superqstate, qdata):
    return True

def operate(id, event, qstate, qdata):
    
    if (event == MODULE_EVENT_NEW) or (event == MODULE_EVENT_PASS):
        qdn = qstate.qinfo.qname_str
        qdn_no_dot = qdn.rstrip('.')
        #log_info("[module][operate][event]: query: %s"%(qdn_no_dot))
	 	

        msg = DNSMessage(qdn, RR_TYPE_TXT, RR_CLASS_IN, PKT_QR | PKT_RA | PKT_AA)
        if (qstate.qinfo.qtype == RR_TYPE_TXT) or (qstate.qinfo.qtype == RR_TYPE_ANY):  
            return False
			 
        # Set qstate.return_msg 
        if not msg.set_return_msg(qstate):
           #log_info("STATE ERROR")
           qstate.ext_state[id] = MODULE_ERROR 
           return True
	    
        # Instantiate the class
        validator = QueryValidator(qdn_no_dot)
	        

        # Check for blacklisted result
        if validator.should_block():
            qstate.return_rcode = RCODE_REFUSED
            qstate.return_msg.rep.security = 2
            qstate.ext_state[id] = MODULE_FINISHED	
            return True	      
 
        # Pass the query to validator
        qstate.ext_state[id] = MODULE_WAIT_MODULE 
        return True
    
    # Module is done	
    if event == MODULE_EVENT_MODDONE:
        #log_info("DONE")
        qstate.ext_state[id] = MODULE_FINISHED 
        return True
    
    log_info("BAD EVENT")
    qstate.ext_state[id] = MODULE_ERROR
    return True

