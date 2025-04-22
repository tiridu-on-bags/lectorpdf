<script lang="ts">
  import { onMount } from 'svelte';
  
  // Estados para interactividad
  let isMenuOpen = false;
  
  // Función para manejo de CTA principal
  const handlePruebaGratis = () => {
    // Implementar lógica para inicio de prueba gratuita
    console.log('Iniciando prueba gratuita');
  };
</script>

<div class="min-h-screen bg-gray-50">
  <!-- Header con navegación principal -->

  <!-- Sección Hero -->
  <section class="py-16 md:py-24 px-4">
    <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center">
      <div class="md:w-1/2 mb-10 md:mb-0">
        <h1 class="text-4xl md:text-5xl font-bold text-[#2c332d] leading-tight mb-6">
          ¿Ahogado en PDFs? Tu Lector Inteligente para Entender Más Rápido.
        </h1>
        <p class="text-lg text-gray-700 mb-8">
          Extrae ideas clave, aclara dudas y encuentra respuestas sin esfuerzo.
          La IA que necesitas, integrada directamente en tu lector de PDF del navegador.
        </p>
        <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
          <button 
            on:click={handlePruebaGratis}
            class="bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 transition shadow-md"
          >
            Prueba PDFlex Gratis
          </button>
          <button 
            class="border border-gray-300 bg-white text-gray-700 py-3 px-6 rounded-md font-semibold hover:bg-gray-50 transition flex items-center justify-center"
          >
            <span class="mr-2">▶</span> Ver Demo Rápida
          </button>
        </div>
      </div>
      <div class="md:w-1/2">
        <div class="bg-white p-4 rounded-lg shadow-xl border border-gray-200">
          <div class="bg-blue-50 p-2 rounded-t-lg border-b border-blue-100 flex items-center mb-3">
            <div class="w-3 h-3 rounded-full bg-red-400 mr-1"></div>
            <div class="w-3 h-3 rounded-full bg-yellow-400 mr-1"></div>
            <div class="w-3 h-3 rounded-full bg-green-400 mr-2"></div>
            <span class="text-sm text-gray-500">Informe_Trimestral_Q2_2023.pdf</span>
          </div>
          <div class="py-4 px-6 rounded-lg bg-gray-50">
            <h3 class="font-bold mb-2 text-gray-800">Resumen Ejecutivo</h3>
            <p class="text-gray-700 text-sm">
              El segundo trimestre de 2023 ha mostrado resultados positivos en todas las áreas
              de negocio, con un crecimiento del 12% en comparación con el mismo período del año
              anterior.
            </p>
            <p class="text-gray-700 text-sm mt-2">
              El análisis de mercado indica que nuestra estrategia de expansión regional ha sido
              efectiva, resultando en un aumento del 18% en nuevos clientes y una retención del
              94% de la base existente.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Características Principales -->
  <section id="caracteristicas" class="py-16 bg-white px-4">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-3xl font-bold text-center mb-12 text-[#2c332d]">
        Presentamos PDFlex: La Forma Inteligente y Simple de Leer PDFs
      </h2>
      <p class="text-center text-lg text-gray-700 mb-12 max-w-3xl mx-auto">
        PDFlex transforma tu lector de PDF habitual. Integra un asistente IA directamente
        en tu flujo de trabajo. Selecciona cualquier texto y obtén al instante:
      </p>
      
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Tarjeta 1: Resume -->
        <div class="bg-gray-50 rounded-lg p-6 shadow-sm hover:shadow-md transition">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
              <span class="text-xl font-bold">1</span>
            </div>
          </div>
          <h3 class="text-xl font-semibold text-center mb-2">Resume al Instante</h3>
          <p class="text-gray-600 text-center">
            Convierte párrafos o páginas enteras en puntos clave en segundos. Perfecto para
            informes, artículos y contratos.
          </p>
        </div>
        
        <!-- Tarjeta 2: Explica -->
        <div class="bg-gray-50 rounded-lg p-6 shadow-sm hover:shadow-md transition">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
              <span class="text-xl font-bold">2</span>
            </div>
          </div>
          <h3 class="text-xl font-semibold text-center mb-2">Explica con Claridad</h3>
          <p class="text-gray-600 text-center">
            Desomplica jerga técnica, legal o conceptos difíciles. Entiende todo sin buscar fuera del
            documento.
          </p>
        </div>
        
        <!-- Tarjeta 3: Pregunta -->
        <div class="bg-gray-50 rounded-lg p-6 shadow-sm hover:shadow-md transition">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
              <span class="text-xl font-bold">3</span>
            </div>
          </div>
          <h3 class="text-xl font-semibold text-center mb-2">Pregunta y Encuentra Rápido</h3>
          <p class="text-gray-600 text-center">
            ¿Buscas un dato específico? Pregúntale directamente al texto seleccionado. Obtén respuestas
            precisas al momento.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Cómo Funciona -->
  <section id="comofunciona" class="py-16 bg-gray-50 px-4">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-3xl font-bold text-center mb-4 text-[#2c332d]">
        Tan Fácil Como Seleccionar Texto
      </h2>
      <p class="text-center text-lg text-gray-700 mb-12 max-w-3xl mx-auto">
        Sin configuraciones complejas ni curvas de aprendizaje. Empieza a usarlo en segundos.
      </p>
      
      <div class="grid md:grid-cols-3 gap-8 mb-12">
        <!-- Paso 1 -->
        <div class="relative">
          <div class="absolute -top-2 -left-2 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">1</div>
          <div class="bg-white rounded-lg p-6 shadow-md h-full">
            <h3 class="text-xl font-semibold mb-3">Abre tu PDF</h3>
            <p class="text-gray-600">
              Carga cualquier documento PDF en tu navegador usando PDFlex.
            </p>
            <div class="mt-6 bg-gray-100 rounded-lg p-4 flex items-center justify-center h-32">
              <div class="text-6xl text-gray-400">📄</div>
            </div>
          </div>
        </div>
        
        <!-- Paso 2 -->
        <div class="relative">
          <div class="absolute -top-2 -left-2 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">2</div>
          <div class="bg-white rounded-lg p-6 shadow-md h-full">
            <h3 class="text-xl font-semibold mb-3">Selecciona el Texto</h3>
            <p class="text-gray-600">
              Marca el texto que necesitas procesar o entender mejor.
            </p>
            <div class="mt-6 bg-gray-100 rounded-lg p-4 flex items-center justify-center h-32">
              <div class="text-6xl text-gray-400">✏️</div>
            </div>
          </div>
        </div>
        
        <!-- Paso 3 -->
        <div class="relative">
          <div class="absolute -top-2 -left-2 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">3</div>
          <div class="bg-white rounded-lg p-6 shadow-md h-full">
            <h3 class="text-xl font-semibold mb-3">Elige la Acción IA</h3>
            <p class="text-gray-600">
              Selecciona resumir, explicar o preguntar en el menú contextual. ¡Listo!
            </p>
            <div class="mt-6 bg-gray-100 rounded-lg p-4 flex items-center justify-center h-32">
              <div class="text-6xl text-gray-400">💡</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Demostración -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="p-4 bg-gray-100 border-b border-gray-200">
          <p class="font-medium text-gray-700">Ejemplo de uso de PDFlex</p>
        </div>
        <div class="p-6 flex justify-center">
          <div class="w-full h-64 bg-gray-200 rounded flex items-center justify-center">
            <p class="text-gray-500">Vista previa de la herramienta</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Para quién es ideal -->
  <section id="usuarios" class="py-16 bg-white px-4">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-3xl font-bold text-center mb-4 text-[#2c332d]">
        Ideal para Profesionales y Estudiantes en Latinoamérica
      </h2>
      <p class="text-center text-lg text-gray-700 mb-12 max-w-3xl mx-auto">
        Si eres Coordinador de Proyectos, Analista, Consultor, Abogado, Investigador,
        Estudiante o simplemente necesitas ser más eficiente con tus documentos, PDFlex
        es para ti.
      </p>
      
      <div class="grid md:grid-cols-4 gap-6">
        <!-- Analistas -->
        <div class="p-6 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
              <span class="font-bold">A</span>
            </div>
          </div>
          <h3 class="text-lg font-semibold text-center mb-2">Analistas de Mercado</h3>
          <p class="text-gray-600 text-sm text-center">
            Analiza informes de mercado más rápido y extrae insights clave para tomar decisiones
            informadas.
          </p>
        </div>
        
        <!-- Ejecutivos -->
        <div class="p-6 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
              <span class="font-bold">E</span>
            </div>
          </div>
          <h3 class="text-lg font-semibold text-center mb-2">Ejecutivos y Gerentes</h3>
          <p class="text-gray-600 text-sm text-center">
            Prepara reuniones eficientemente y extrae los puntos clave de
            reportes extensos.
          </p>
        </div>
        
        <!-- Abogados -->
        <div class="p-6 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
              <span class="font-bold">L</span>
            </div>
          </div>
          <h3 class="text-lg font-semibold text-center mb-2">Abogados</h3>
          <p class="text-gray-600 text-sm text-center">
            Revisa cláusulas de contratos clave al instante y simplifica la comprensión de
            documentos legales complejos.
          </p>
        </div>
        
        <!-- Estudiantes -->
        <div class="p-6 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
              <span class="font-bold">S</span>
            </div>
          </div>
          <h3 class="text-lg font-semibold text-center mb-2">Estudiantes</h3>
          <p class="text-gray-600 text-sm text-center">
            Estudia para tus exámenes sin agobios y comprende mejor textos académicos complejos.
          </p>
        </div>
      </div>
      
      <!-- Testimonial -->
      <div class="mt-16 bg-gray-50 rounded-lg p-8 shadow-sm border border-gray-200">
        <div class="flex flex-col items-center">
          <p class="text-gray-700 text-center mb-4 italic">
            "PDFlex ha transformado mi forma de trabajar con documentos. Ahora puedo
            revisar informes en la mitad del tiempo y extraer exactamente lo que necesito."
          </p>
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mr-3">
              JM
            </div>
            <div>
              <p class="font-medium">Javier Méndez</p>
              <p class="text-sm text-gray-500">Gerente de Proyectos, Ciudad de México</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Final -->
  <section class="py-16 bg-[#2c332d] px-4">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-3xl font-bold text-[#f9f4e9] mb-6">
        Comienza a Ahorrar Tiempo Hoy Mismo
      </h2>
      <p class="text-lg text-gray-300 mb-8">
        Prueba PDFlex gratis y descubre cómo puedes procesar documentos PDF de forma más eficiente que nunca.
      </p>
      <button class="bg-blue-600 text-white py-3 px-8 rounded-md font-semibold hover:bg-blue-700 transition shadow-lg text-lg">
        Prueba PDFlex Gratis
      </button>
      <p class="text-gray-400 mt-4">No se requiere tarjeta de crédito</p>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-gray-900 text-gray-400 py-12 px-4">
    <div class="max-w-6xl mx-auto grid md:grid-cols-4 gap-8">
      <div>
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-[#f9f4e9] rounded-full flex items-center justify-center mr-2">
            <span class="text-[#2c332d] font-bold">PDF</span>
          </div>
          <span class="font-bold text-white text-lg">PDFlex</span>
        </div>
        <p class="text-sm">
          Tu asistente inteligente para la lectura y comprensión de documentos PDF.
        </p>
      </div>
      
      <div>
        <h3 class="font-semibold text-white mb-4">Producto</h3>
        <ul class="space-y-2">
          <li><a href="#" class="hover:text-white transition">Características</a></li>
          <li><a href="#" class="hover:text-white transition">Precios</a></li>
          <li><a href="#" class="hover:text-white transition">Demo</a></li>
          <li><a href="#" class="hover:text-white transition">Casos de Uso</a></li>
        </ul>
      </div>
      
      <div>
        <h3 class="font-semibold text-white mb-4">Recursos</h3>
        <ul class="space-y-2">
          <li><a href="#" class="hover:text-white transition">Centro de Ayuda</a></li>
          <li><a href="#" class="hover:text-white transition">Blog</a></li>
          <li><a href="#" class="hover:text-white transition">Tutoriales</a></li>
          <li><a href="#" class="hover:text-white transition">API</a></li>
        </ul>
      </div>
      
      <div>
        <h3 class="font-semibold text-white mb-4">Empresa</h3>
        <ul class="space-y-2">
          <li><a href="#" class="hover:text-white transition">Acerca de</a></li>
          <li><a href="#" class="hover:text-white transition">Contacto</a></li>
          <li><a href="#" class="hover:text-white transition">Política de Privacidad</a></li>
          <li><a href="#" class="hover:text-white transition">Términos de Servicio</a></li>
        </ul>
      </div>
    </div>
    
    <div class="max-w-6xl mx-auto mt-12 pt-8 border-t border-gray-800 text-center">
      <p>© 2025 PDFlex. Todos los derechos reservados.</p>
    </div>
  </footer>
</div> 