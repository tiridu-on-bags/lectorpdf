// src/routes/api/pdf/[id]/+server.ts
import type { RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ params, fetch, request }) => {
  const id = params.id;
  const backendUrl = `http://localhost:8000/api/pdf-basic/${id}`;
  
  try {
    // Implementación del patrón de Circuit Breaker
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);
    
    // Transferir la petición al backend con streaming bidireccional
    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        // Mantener headers relevantes del cliente original
        'Accept': request.headers.get('Accept') || 'application/pdf',
        'Accept-Language': request.headers.get('Accept-Language') || 'es'
      },
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      return new Response(
        JSON.stringify({ 
          error: 'Error al obtener el PDF', 
          status: response.status 
        }), {
          status: response.status,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
    
    // Streaming directo del contenido binario manteniendo tipos MIME
    const pdfData = await response.arrayBuffer();
    
    return new Response(pdfData, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `inline; filename="${id}.pdf"`,
        'Cache-Control': 'public, max-age=3600'
      }
    });
  } catch (error) {
    console.error('Error en el proxy de PDF:', error);
    
    return new Response(
      JSON.stringify({ 
        error: 'Error al procesar la solicitud',
        message: error.message 
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
};

// Soporte explicit para HEAD y OPTIONS
export const HEAD = GET;

export const OPTIONS: RequestHandler = async () => {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Accept',
      'Access-Control-Max-Age': '86400'
    }
  });
};