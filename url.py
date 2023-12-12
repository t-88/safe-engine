import socket
import ssl

# NOTE: maybe implement https protocol from scratch for now i am using ssl  


class URL():
    def __init__(self,url : str):
        url =  url if url[-1] != "/" else url[:-1] # remove / in the end of the url
        self.url = url  

        self.port = 80 
        self.page_path = ""

        # get protocol http or https
        self.protocol , url = url.split("://",1)
        assert self.protocol in ["http","https"]



        # get host addr and page_path
        if "/" in url: url , self.page_path = url.split("/",1)
        if ":" in url: url , self.port = url.split(":",1)

        self.port = int(self.port)
        self.host = url

        if self.protocol == "https":
            self.port = 443  # https port


        # const request to get the html page
        self.get_request = f"GET /{self.page_path} HTTP/1.0\nHost: {self.host}\n\n".encode()
        
    def print_state(self):
        print("url: ",self.url)
        print("host: ",self.host)
        print("port: ",self.port)
        print("protocol: ",self.protocol)
        print("page_path: ",self.page_path)
        print("get-request: ",self.get_request)
    
    def request(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # handle https using ssl
        if self.protocol == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s,server_hostname=self.host)


        try:
            s.connect((self.host,self.port))
        except Exception as e:
            print(e)
            print(f"[ERROR] Failed to connect to {self.host}")
            print("port:",self.port)
            print("path:",self.page_path)
            exit(-1)
        
        s.sendall(self.get_request)
        response = s.makefile("r",encoding="utf-8",newline="\r\n")
        s.close()


        self.http_version, self.status_code , _ =  response.readline().split(" ",2)


        self.response_headers = {} 
        while True:
            line =  response.readline()
            if line == "\r\n": break

            key,  value =  line.split(":",1)
            value = value.strip()
            key = key.lower()

            self.response_headers[key] = value
        
        self.response_headers["body"] =  response.read(int(self.response_headers["content-length"]))

        # for compression read more https://browser.engineering/http.html
        # TODO: i happen to be intersted in compression so implement smth simple (https://github.com/t-88/compression-algorithms)
        
        assert "transfer-encoding" not in self.response_headers 
        assert "content-encoding" not in self.response_headers 

        response.close()

        return self.response_headers["body"]