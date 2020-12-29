from fastapi import FastAPI
from pydantic import BaseModel
from numpy import sign
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.
class eliminate(BaseModel):
    A:list
    b:list

class interpolation(BaseModel):
    x:int
    xi:list
    yi:list

class differentiation(BaseModel):
    h:float
    p:int

class integration(BaseModel):
    a:int
    b:int

class rootFinding(BaseModel):
    a:float
    b:float
    dx:float


origins = [
    "*",
    "https://commath-phattaraphon.herokuapp.com",
    "https://commath-phattaraphon.herokuapp.com/b2s",
    "https://commath-phattaraphon.herokuapp.com/elimination",
    "https://commath-phattaraphon.herokuapp.com/interpolation",
    "https://commath-phattaraphon.herokuapp.com/differentiation",
    "https://commath-phattaraphon.herokuapp.com/integration",
    "https://commath-phattaraphon.herokuapp.com/root-finding"

]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"111111"}
@app.get("/b2s/{text}")
def bit2int(text:str):
    s = int(text[0])
    e = int(text[1:9], 2)
    f = [ int(x) for x in text[9:]]
    x = 1 + sum([ int(f[i])*2**(-(i+1)) for i in range(len(f)) ])
    result = (-1)**s * 2**(e-127) * x 
    return result
@app.post("/elimination")
def api(data:eliminate):
    lam = int(data.A[1][0]) / int(data.A[0][0])
    data.A[1] = [ int(x)-lam*int(y) for x,y in zip(data.A[1],data.A[0]) ]
    data.b[1] = int(data.b[1]) - lam*int(data.b[0])
 
    lam = int(data.A[2][0]) / int(data.A[0][0])
    data.A[2] = [ int(x)-lam*int(y) for x,y in zip(data.A[2],data.A[0]) ]
    data.b[2] = int(data.b[2]) - lam*int(data.b[0])
 
    lam = int(data.A[2][1]) / int(data.A[1][1])
    data.A[2] = [ int(x)-lam*int(y) for x,y in zip(data.A[2],data.A[1]) ]
    data.b[2] = int(data.b[2]) - lam*int(data.b[1])

    x2 = int(data.b[2])/int(data.A[2][2])
    x1 = (int(data.b[1]) - int(data.A[1][2])*x2)/int(data.A[1][1])
    x0 = (int(data.b[0]) - int(data.A[0][1])*x1 - int(data.A[0][2])*x2)/int(data.A[0][0])

    result = [x0,x1,x2]
    return result

@app.post("/interpolation")
def api(data:interpolation):
    def Li(i, x, xi, yi):
        L = 1
        for j in range(len(xi)):
            if j != i:
                L = L*(x-int(xi[j]))/(int(xi[i])-int(xi[j]))
        return L
    def lin(x, xi, yi):
        return sum([ int(yi[i])*Li(i,x,xi,yi) for i in range(len(xi)) ])
    
    return lin(int(data.x),data.xi,data.yi)


@app.post("/differentiation")
def api(data:differentiation):
    def g(h):
        cda = {
            0.64: 0.380610   ,
            0.32: 0.371035   ,
            0.16: 0.368711   ,
            0.08: 0.368281   ,
            0.04: 0.36875    ,
            0.02: 0.37       ,
            0.01: 0.38       ,
            0.005: 0.40       ,
            0.0025: 0.48       ,
            0.00125: 1.28      ,
        }
        return cda[h]

    def richex(h, p):
        return ((2**p)* g(h/2)- g(h))/(2**p - 1)
    
    return richex(float(data.h),int(data.p))

@app.post("/integration")
def api(data:integration):
    def f(x): return 3*x**2 + 9*x + 2
    def simpson(f, a, b):
        n = 4
        x0 = a
        h = (b-a)/n
        return (f(x0+0*h) + 4*f(x0+1*h) + 2*f(x0+2*h) + 4*f(x0+3*h) + f(x0+4*h))*h/3
    
    return simpson(f, int(data.a), int(data.b))


@app.post("/root-finding")
def api(data:rootFinding):
    def f(x):
        return x**3 - 10.0*x**2 + 5.0

    def rootsearch(f,a,b,dx):
        x1, f1 = a, f(a)
        x2, f2 = a+dx, f(a+dx)
        while sign(f1) == sign(f2):
           if x1 >= b: return None,None
           x1 = x2; f1 = f2
           x2 = x1 + dx; f2 = f(x2)

        return "("+str(x1)+", "+str(x2)+")"
    return rootsearch(f,float(data.a),float(data.b),float(data.dx))