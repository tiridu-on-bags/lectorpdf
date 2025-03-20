#Configurar el entorno backend antes de usar

## Correr el script api.py


#Para el fronted installar npm 


## npm install
## npm run dev



# Diseño 

Frontend (SvelteKit): Se encarga de la interfaz de usuario y la interacción con el usuario. SvelteKit es una excelente opción por su rendimiento y experiencia de desarrollo.
API Gateway (FastAPI): Actúa como un punto de entrada único para todas las solicitudes del frontend. FastAPI es una muy buena elección para construir APIs en Python por su velocidad, validación de datos y documentación automática.
Servicios ML: Este componente encapsula la lógica de aprendizaje automático, que incluiría el procesamiento del PDF y la interacción con el LLM. Esto mantiene la lógica de ML separada de la interfaz y el gateway.
Almacenamiento (S3): Utilizar un servicio de almacenamiento en la nube como S3 para guardar los archivos PDF es una práctica recomendada por su escalabilidad y durabilidad.
Sistemas de Monitoreo: Incluir sistemas de monitoreo desde el inicio es crucial para observar el rendimiento de la aplicación, detectar errores y entender el uso.
