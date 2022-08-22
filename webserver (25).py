from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi


#starting task list as placeholder
tasklist = ['Add Tasks, Use the X to Delete Task']

#request handler that deals with different paths, calls on BaseHTTPRequestHandler
class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
      if self.path.endswith('/tasklist'):
        #if path ends with task list, then create the home page of displaying Task List and 3 placeholder tasks  
          self.send_response(200)
          self.send_header('content-type', 'text/html')
          self.end_headers()
      
          output = ''
          output +='<html><body>'
          output+= '<h1>To Do List </h1>'
          output+='<h3><a href = "/tasklist/new"> Add New Task</a></h3>'
          #new task creator button, redirects to creating path
          for task in tasklist:
            output += task
            output += ' ';
            output += '<a/ href = "/tasklist/%s/bold" >Prioritize</a>' % task
            output += ' ';
            output += '<a/ href = "/tasklist/%s/remove" >X</a>' %task
            #option to remove task, redirects to deleting path
            output += '</br>'
      
          output += '</body></html>'
          self.wfile.write(output.encode())

      if self.path.endswith('/new'):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        output = ''
        output += '<html><body>' 
        output +='<h1>Add New Task </h1>'
        output +='<form method = "Post" enctype = "multipart/form-data" action = "/tasklist/new">'
        output += '<input name = "task" type = "text" placeholder = "Add new task">'
        output += '<input type = "submit" value = "Add">'
        output += '</form>'
        output += '</body></html>'
        self.wfile.write(output.encode())

      if self.path.endswith('/bold'):
        listIDPath = self.path.split('/')[2]
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        output = ''
        output +='<html><body>'
        output +='<h1>Prioritize task: %s </h1>'% listIDPath
        #changes paths to remove path
        output += '<form method = "POST" enctype = "multipart/form-data" action="/tasklist/%s/bold">' % listIDPath.replace('%20', ' ');
        output += '<input type = "submit" value ="Move to the front"></form>'
        output += '<a href =" /tasklist"> Cancel </a>'
        output +='</body></html>'
        self.wfile.write(output.encode())

      if self.path.endswith('/remove'):
        listIDPath = self.path.split('/')[2]
        print(listIDPath)
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        output = ''
        output +='<html><body>'
        output +='<h1>Remove task: %s </h1>'% listIDPath.replace('%20', ' ');
        #changes paths to remove path
        output += '<form method = "POST" enctype = "multipart/form-data" action="/tasklist/%s/remove">' % listIDPath
        output += '<input type = "submit" value ="Remove"></form>'
        output += '<a href =" /tasklist"> Cancel </a>'
        output +='</body></html>'
        self.wfile.write(output.encode())

    def do_POST(self):
      if self.path.endswith('/new'):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'],"utf-8")
        content_len = int(self.headers.get('Content-length'))
        pdict['CONTENT-LENGTH'] = content_len
                          
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile,pdict)
          new_task = fields.get('task')
          tasklist.append(new_task[0])
      self.send_response(301)
      self.send_header('content-type','text/html')
      self.send_header('Location','/tasklist')
      self.end_headers()

      if self.path.endswith('/remove'):
        #removes the list by replacing it within task list folder
        listIDPath = self.path.split('/')[2]
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
          list_item = listIDPath.replace('%20',' ')
          tasklist.remove(list_item)

        self.send_response(301)
        self.send_header('content-type','text/html')
        self.send_header('Location','/tasklist')
        self.end_headers()

      if self.path.endswith('/bold'):
        #removes the list by replacing it within task list folder
        listIDPath = self.path.split('/')[2]
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
          list_item = listIDPath.replace('%20',' ')
          tasklist.remove(list_item)
          tasklist.insert(0,list_item)

        self.send_response(301)
        self.send_header('content-type','text/html')
        self.send_header('Location','/tasklist')
        self.end_headers()

          

#main method which runs server forever
def main():
    PORT = 8000
    server = HTTPServer(('', PORT), requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

#calls on main server if the handler is the same
if __name__ == '__main__':
    main()