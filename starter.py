"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
import os
from app.app import create_app
# development
app = create_app(environment='development') if(os.path.exists('.dev')) else create_app(environment='production')

@app.route('/', methods=['GET'], strict_slashes=False)
def lin_slogan():
    return """<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor: 
    pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family: 
    "Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal; 
    margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"><p> 
    Python Success <br/><span style="font-size:30px">心上无垢，林间有风。</span></p></div> """

if __name__ == '__main__':
    app.run(port=4000)
