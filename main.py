from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

#-----------------------
# Modelo de validaciones 
#-----------------------
class Producto(BaseModel):
    nombre: str = Field(..., min_length=3)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str

#-------------------------
#Almacenamiento en memoria
#-------------------------
Productos = []

#---------------------
#Endpoint inicial
#---------------------
@app.post("/productos")
def crear_producto(producto: Producto):         
    for p in Productos:
        if p.nombre == producto.nombre:
            raise HTTPException(status_code=400, detail="El producto ya existe")
    
    Productos.append(producto)
    return {"mensaje": "Producto creado"}

#-------------------
#Obtener todos
#-------------------
@app.get ("/productos")
def obtener_productos(): 
    return Productos 

#-------------------
#Obtener uno 
#-------------------
@app.get("/productos/{nombre}")
def obtener_producto(nombre: str):
    for p in Productos: 
        if p.nombre == nombre:
            return p 
    raise HTTPException(status_code=404, detail="Producto no encontrado")

#--------------------
#Actualizar producto
#--------------------
@app.put("/productos/{nombre}")
def actualizar_producto(nombre: str, producto_actualizado: Producto):
    for i, p in enumerate(Productos):
        if p.nombre == nombre:
            Productos[i] = producto_actualizado
            return {"mensaje": "Producto actualizado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

#---------------------
#Eliminar producto
#---------------------
@app.delete("/productos/{nombre}")
def eliminar_producto(nombre: str):
    for i, p in enumerate(Productos):
        if p.nombre == nombre:
            Productos.pop(i)
            return {"mensaje": "Producto eliminado"}
        
    raise HTTPException(status_code=404, detail="Producto no encontrado")

#----------------------
#Filtrar por categoria
#----------------------
@app.get("/productos/categoria/{categoria}")
def productos_por_categoria(categoria: str):
    resultado = [p for p in Productos if p.categoria == categoria]
    return resultado 
        