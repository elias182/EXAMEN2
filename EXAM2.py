import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try: 
    data = pd.read_excel("InventarioTechZone.xlsx")




except FileNotFoundError:
    st.error("El archivo 'InventarioTechZone.xlsx' no se encuentra en el directorio actual. Por favor, asegúrate de que el archivo esté presente.")
    st.stop()  # Detener la ejecución si el archivo no se encuentra


def nuevo_producto(nuevo_producto):
    nuevo_producto["valorTotal"] = nuevo_producto["Precio"] * nuevo_producto["Stock"]
    nuevo_producto["margenGanancia"] = nuevo_producto["Precio"] * 0.12
    nuevo_producto["diasEnInventario"] = (pd.Timestamp.now() - nuevo_producto["FechaIngreso"]).dt.days
    if nuevo_producto["Stock"] > 5:
        nuevo_producto["Estado"] = "Disponible"
    elif nuevo_producto["Stock"] <= 5 and nuevo_producto["Stock"] > 0:
        nuevo_producto["Estado"] = "Critico"
    else:
        nuevo_producto["Estado"] = "Agotado"
    if nombre == "" or precio <= 0 or stock < 0:
        st.error("El nombre del producto no puede estar vacío")
    else:
        data = pd.concat([data, nuevo_producto], ignore_index=True)
        st.success("Producto añadido correctamente")
    

#convertir la columna 'Fecha de Ingreso' a tipo datetime
data['FechaIngreso'] = pd.to_datetime(data['FechaIngreso'])

# filtro por categoria una o varias
categorias = st.multiselect("Selecciona las categorías", options=data['Categoria'].unique())

estado = st.selectbox("Selecciona el estado", options=data['Estado'].unique())

precio = st.slider("Selecciona el rango de precio", min_value=float(data['Precio'].min()), max_value=float(data['Precio'].max()), value=(float(data['Precio'].min()), float(data['Precio'].max())))

busqueda = st.text_input("Buscar por nombre de producto")

stockmin = st.checkbox("Mostrar solo productos con stock mínimo")

if categorias:
    data = data[data['Categoria'].isin(categorias)]

if estado:
    data = data[data['Estado'] == estado]

if precio:
    data = data[(data['Precio'] >= precio[0]) & (data['Precio'] <= precio[1])]

if busqueda:
    data = data[data['Producto'].str.contains(busqueda, case=False, na=False)]

if stockmin:
    data = data[data['Stock'] > 0]

data["valorTotal"] = data["Precio"] * data["Stock"]

data["margenGanancia"] = data["Precio"] * 0.12

data["diasEnInventario"] = (pd.Timestamp.now() - data["FechaIngreso"]).dt.days

st.dataframe(data)


st.header("Añadir nuevo producto")

nombre = st.text_input("Nombre del producto")
categoria = st.selectbox("Categoría", options=data['Categoria'].unique())
precio = st.number_input("Precio", min_value=0.0, value=0.0)
stock = st.number_input("Stock", min_value=0, value=0)

if st.button("Añadir producto"):
    nuevo_producto = pd.DataFrame({
        "Producto": [nombre],
        "Categoria": [categoria],
        "Precio": [precio],
        "Stock": [stock],
        "FechaIngreso": [pd.Timestamp.now()]
    })
    nuevo_producto(nuevo_producto)



cantproductos = data.groupby("Categoria")["Producto"].count()
VTporCategoria = data.groupby("Categoria")["valorTotal"].sum()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

ax1.bar(cantproductos.index, cantproductos.values)
ax1.set_title("Cantidad de productos por categoría")
ax1.set_xlabel("Categoría")
ax1.set_ylabel("Cantidad de productos")
ax1.tick_params(axis='x', rotation=45)

ax2.pie(VTporCategoria, labels=VTporCategoria.index, autopct='%1.1f%%', startangle=90)
ax2.set_title("Valor total por categoría")

plt.tight_layout()
st.pyplot(fig)

top5productos = data.nlargest(5, "valorTotal")[["Producto", "valorTotal"]]
st.write("### Top 5 productos con mayor valor total")
fig = plt.figure(figsize=(10, 5))
plt.bar(top5productos["Producto"], top5productos["valorTotal"])
plt.title("Top 5 productos con mayor valor total")
plt.xlabel("Producto")
plt.ylabel("Valor Total")
plt.xticks(rotation=45)
st.pyplot(fig)




















