class DSSnet_hosts:
    'class for meta process/IED info'
    p_id = 0
    
    def __init__(self, msg, IED_id, command, ip):
        self.properties= msg
        self.IED_id     = IED_id
        self.process_id= DSSnet_hosts.p_id
        self.command = command
        self.ip = ip
        DSSnet_hosts.p_id +=1
    
    def number_processes(self):
        return DSSnet_hosts.p_id

    def get_host_name(self):
        return self.IED_id

    def get_ip(self):
        return self.ip
    
    def get_process_command(self):
        return self.command

    def display_process(self):
        return('%s : %s : %s \n' % (self.process_id , self.IED_id, self.properties))
                       
