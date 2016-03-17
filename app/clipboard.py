@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def home_page():
    logging.debug('/index GET')
    form = InputURLform(request.form)

    # this is activated when the form is filled POSTed by user
    if form.validate_on_submit():
        logging.debug('/indexPOST')
        entered_url = form.url.data
        logging.debug(entered_url)
        return render_template('showPg.html', 
                           title='input URL POST',
                           url=entered_url)

    # this is activated for the first round
    return render_template('inputURLform.html',
                            title='input URL GET',
                            form=form)

    def home_page():
    logging.debug('/index GET')
    form = InputURLform(request.form)

    # this is activated when the form is filled POSTed by user
    if form.validate_on_submit():
        logging.debug('/indexPOST')
        entered_url = form.url.data
        logging.debug(entered_url)

        try: 
          logging.debug('/index/POST/Try1')
          response = urllib2.urlopen(entered_url)
          logging.debug('RESPONSE:', response)
          logging.debug('URL     :', response.geturl())
          print ('RESPONSE:', response, file=sys.stderr)
          print ('URL     :', response.geturl(), file=sys.stderr)

          headers = response.info()
          print ('DATE    :', headers['date'], file=sys.stderr)
          print ('HEADERS :', file=sys.stderr)
          print ('---------', file=sys.stderr)
          print (headers, file=sys.stderr)

          data = response.read()
          print ('LENGTH  :', len(data), file=sys.stderr)
          print ('DATA    :', file=sys.stderr)
          print ('---------', file=sys.stderr)
          print (data, file=sys.stderr)
        except urllib2.URLError:
            return render_template('error.html', eCode='URLError in trying to open a URL through urllibe2.urlopen()')
        except ValueError:
            return render_template('error.html', eCode='ValueError in trying to open a URL through urllibe2.urlopen(). Entered URL is apparently is malformed.')    


        return render_template('showPg.html', 
                           title='input URL POST',
                           url=entered_url)

    # this is activated for the first round
    return render_template('inputURLform.html',
                            title='input URL GET',
                            form=form)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def home_page():
    logging.debug('/index GET')
    form = InputURLform(request.form)

    # this is activated when the form is filled POSTed by user
    if form.validate_on_submit():
       logging.debug('/indexPOST')
       entered_url = form.url.data
       logging.debug(entered_url)

       try: 
         logging.debug('/index/POST/Try1')
         response = urllib2.urlopen(entered_url)

         # ensure there is no redirection in the URL source page
         if response.geturl() != entered_url:
            return render_template('error.html', eCode='There was a server redirect in urllibe2.urlopen()')
         else:
            page = response.read()
            response.close()
       except urllib2.URLError:
         return render_template('error.html', eCode='URLError in trying to open a URL through urllibe2.urlopen()')
       except ValueError:
         return render_template('error.html', eCode='ValueError in trying to open a URL through urllibe2.urlopen(). Entered URL is apparently is malformed.')    

       # Hack to fix improperly displayed chars on wikipedia.
       try:
          logging.debug('in 2 try')
          page = unicode(page, 'utf-8')  
       except UnicodeDecodeError:
          pass  # Some pages may not need be utf-8'ed

       # Sometimes creators of the page lie about the encoding, thus leading to this execption. 
       # http://lxml.de/parsing.html#python-unicode-strings
       try:
          logging.debug('in 3 try')
          g.root = lxml.html.parse(StringIO.StringIO(page)).getroot()
       except ValueError:
          g.root = lxml.html.parse(entered_url).getroot()  

        
       return render_template('showPg.html', 
                           title='input URL POST',
                           url=entered_url)

    # this is activated for the first round
    return render_template('inputURLform.html',
                            title='input URL GET',
                            form=form)


    #######################3 Show page

{% extends "coreLayout.html" %}
{% block body %}
   <p> 
   I got into the showPg. Here is the {{ url }} that the user wanted.
   </p>
   <iframe frameborder='0' noresize='noresize' style='position: absolute; background: transparent; width: 100%; height:100%;' src= {{ url }} frameborder="0"></iframe>   
{% endblock %}


