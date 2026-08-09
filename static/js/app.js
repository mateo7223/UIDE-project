const productos = [
  {id:1,nombre:'Taladro eléctrico',categoria:'Herramientas',precio:59.99,stock:15,imagen:'https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=700&q=80',descripcion:'Taladro de 650 W con velocidad regulable.'},
  {id:2,nombre:'Pintura interior blanca',categoria:'Pinturas',precio:28.50,stock:24,imagen:'https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=700&q=80',descripcion:'Pintura lavable para interiores, 4 litros.'},
  {id:3,nombre:'Juego de destornilladores',categoria:'Herramientas',precio:18.75,stock:32,imagen:'https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?auto=format&fit=crop&w=700&q=80',descripcion:'Juego de seis destornilladores.'},
  {id:4,nombre:'Cable eléctrico',categoria:'Electricidad',precio:35,stock:18,imagen:'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=700&q=80',descripcion:'Rollo de cable eléctrico de 100 metros.'},
  {id:5,nombre:'Llave para tubería',categoria:'Plomería',precio:22.40,stock:10,imagen:'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?auto=format&fit=crop&w=700&q=80',descripcion:'Llave ajustable de alta resistencia.'},
  {id:6,nombre:'Cemento de uso general',categoria:'Construcción',precio:9.80,stock:60,imagen:'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=700&q=80',descripcion:'Saco de cemento de 50 kg.'}
];

const noticias = [
  {titulo:'Nueva línea de herramientas',fecha:'10 de julio de 2026',texto:'Incorporamos herramientas eléctricas con garantía de doce meses.'},
  {titulo:'Descuento para contratistas',fecha:'5 de julio de 2026',texto:'Precios especiales en compras al por mayor.'},
  {titulo:'Entregas dentro de Quito',fecha:'1 de julio de 2026',texto:'Realizamos entregas rápidas en diferentes sectores.'}
];

const contenedor = document.getElementById('contenedorProductos');
const buscador = document.getElementById('buscadorProducto');
const categoria = document.getElementById('filtroCategoria');
const sinResultados = document.getElementById('mensajeSinResultados');

function mostrarProductos(lista) {
  contenedor.innerHTML = '';
  sinResultados.classList.toggle('oculto', lista.length > 0);

  lista.forEach(p => {
    const article = document.createElement('article');
    article.className = 'producto';
    article.innerHTML = `
      <img src="${p.imagen}" alt="${p.nombre}">
      <div class="producto-contenido">
        <span class="categoria">${p.categoria}</span>
        <h3>${p.nombre}</h3>
        <p>${p.descripcion}</p>
        <strong>$${p.precio.toFixed(2)}</strong>
        <p>Stock: ${p.stock}</p>
        <button class="boton agregar" data-id="${p.id}">Agregar</button>
      </div>`;
    contenedor.appendChild(article);
  });
}

[...new Set(productos.map(p => p.categoria))].sort().forEach(c => {
  const op = document.createElement('option');
  op.value = c;
  op.textContent = c;
  categoria.appendChild(op);
});

function filtrar() {
  const texto = buscador.value.toLowerCase();
  const cat = categoria.value;
  mostrarProductos(
    productos.filter(
      p =>
        (p.nombre.toLowerCase().includes(texto) ||
          p.descripcion.toLowerCase().includes(texto)) &&
        (cat === 'Todas' || p.categoria === cat)
    )
  );
}

buscador.addEventListener('input', filtrar);
categoria.addEventListener('change', filtrar);

contenedor.addEventListener('click', e => {
  const b = e.target.closest('.agregar');
  if (!b) return;
  const p = productos.find(x => x.id === Number(b.dataset.id));
  alert(`${p.nombre} fue agregado correctamente.`);
});

const noticiasCont = document.getElementById('contenedorNoticias');
noticias.forEach(n => {
  const a = document.createElement('article');
  a.className = 'tarjeta';
  a.innerHTML = `<small>${n.fecha}</small><h3>${n.titulo}</h3><p>${n.texto}</p>`;
  noticiasCont.appendChild(a);
});

function mostrarRespuestaFormulario(texto, tipo = 'ok') {
  const respuesta = document.getElementById('respuestaFormulario');
  respuesta.textContent = texto;
  respuesta.classList.remove('oculto', 'mensaje-error');
  if (tipo === 'error') respuesta.classList.add('mensaje-error');
}

function limpiarErroresContacto(form) {
  form.querySelectorAll('input, textarea').forEach(campo => {
    campo.removeAttribute('aria-invalid');
    const error = campo.parentElement.querySelector('.error');
    if (error) error.textContent = '';
  });
}

function mensajeValidacionContacto(campo) {
  if (campo.validity.valueMissing) return 'Este campo es obligatorio.';
  if (campo.validity.typeMismatch) return 'Escriba un correo electrónico válido.';
  if (campo.validity.tooShort) {
    return `Escriba al menos ${campo.minLength} caracteres.`;
  }
  if (campo.validity.tooLong) {
    return `Escriba máximo ${campo.maxLength} caracteres.`;
  }
  return campo.validationMessage || 'Revise este campo.';
}

function mostrarErrorCampo(campo, mensaje) {
  if (!campo) return;
  campo.setAttribute('aria-invalid', 'true');
  const error = campo.parentElement.querySelector('.error');
  if (error) error.textContent = mensaje;
}

document.getElementById('formContacto').addEventListener('submit', async e => {
  e.preventDefault();

  const form = e.currentTarget;
  const boton = document.getElementById('btnGuardarContacto');
  let valido = true;
  let primerCampoInvalido = null;

  limpiarErroresContacto(form);
  form.querySelectorAll('input, textarea').forEach(c => {
    // Evita que un valor compuesto únicamente por espacios se considere válido.
    c.value = c.value.trim();

    if (!c.checkValidity()) {
      mostrarErrorCampo(c, mensajeValidacionContacto(c));
      if (!primerCampoInvalido) primerCampoInvalido = c;
      valido = false;
    }
  });

  if (!valido) {
    primerCampoInvalido.focus();
    return;
  }

  boton.disabled = true;
  boton.textContent = 'Guardando...';
  mostrarRespuestaFormulario('Guardando el mensaje y enviando el acuse de recibido...');

  try {
    const respuesta = await fetch(document.body.dataset.urlContacto, {
      method: 'POST',
      body: new FormData(form),
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });

    const datos = await respuesta.json();

    if (!respuesta.ok || !datos.ok) {
      if (datos.errores) {
        let primerCampoConError = null;
        Object.entries(datos.errores).forEach(([nombre, errores]) => {
          const campo = form.elements.namedItem(nombre);
          const mensaje = errores?.[0]?.message || 'Revise este campo.';
          mostrarErrorCampo(campo, mensaje);
          if (!primerCampoConError && campo) primerCampoConError = campo;
        });
        if (primerCampoConError) primerCampoConError.focus();
      }
      throw new Error(datos.mensaje || 'No se pudo guardar el mensaje.');
    }

    mostrarRespuestaFormulario(datos.mensaje);
    form.reset();
  } catch (error) {
    mostrarRespuestaFormulario(error.message, 'error');
  } finally {
    boton.disabled = false;
    boton.textContent = 'Guardar';
  }
});

function valorSeguro(valor, sufijo = '') {
  return valor === null || valor === undefined ? '--' : `${valor}${sufijo}`;
}

async function consultarClima(ciudad) {
  const estado = document.getElementById('estadoClima');
  const resultado = document.getElementById('resultadoClima');
  const boton = document.getElementById('btnConsultarClima');

  estado.textContent = 'Consultando OpenWeatherMap...';
  estado.classList.remove('estado-error');
  resultado.classList.add('oculto');
  boton.disabled = true;

  try {
    const url = new URL(document.body.dataset.urlClima, window.location.origin);
    url.searchParams.set('ciudad', ciudad);

    const respuesta = await fetch(url);
    const datos = await respuesta.json();

    if (!respuesta.ok || !datos.ok) {
      throw new Error(datos.mensaje || 'No se pudo consultar el clima.');
    }

    const ubicacion = datos.pais ? `${datos.ciudad}, ${datos.pais}` : datos.ciudad;

    document.getElementById('climaCiudad').textContent = ubicacion;
    document.getElementById('climaTemperaturaGrande').textContent =
      valorSeguro(datos.temperatura, ' °C');
    document.getElementById('climaTemperatura').textContent =
      valorSeguro(datos.temperatura, ' °C');
    document.getElementById('climaHumedad').textContent =
      valorSeguro(datos.humedad, ' %');
    document.getElementById('climaDescripcion').textContent =
      datos.descripcion
        ? datos.descripcion.charAt(0).toUpperCase() + datos.descripcion.slice(1)
        : '--';
    document.getElementById('climaViento').textContent =
      valorSeguro(datos.viento, ' m/s');

    resultado.classList.remove('oculto');
    estado.textContent = `Clima actual consultado para ${ubicacion}.`;
  } catch (error) {
    estado.textContent = error.message;
    estado.classList.add('estado-error');
  } finally {
    boton.disabled = false;
  }
}

document.getElementById('formClima').addEventListener('submit', e => {
  e.preventDefault();
  const ciudad = document.getElementById('ciudadClima').value.trim();
  if (ciudad) consultarClima(ciudad);
});

document.getElementById('anioActual').textContent = new Date().getFullYear();
mostrarProductos(productos);

$(document).ready(function() {
  $('#btnMenu').on('click', function() {
    $('#menuPrincipal').slideToggle(250).toggleClass('abierta');
    const abierto = $(this).attr('aria-expanded') === 'true';
    $(this).attr('aria-expanded', String(!abierto));
  });

  $('.nav-link').on('click', function(e) {
    e.preventDefault();
    const destino = $(this).attr('href');
    $('.nav-link').removeClass('activo');
    $(this).addClass('activo');
    $('html,body').animate({scrollTop: $(destino).offset().top - 115}, 550);
  });

  $('#btnOferta').on('click', function() {
    $('#modalOferta')
      .fadeIn(200)
      .addClass('abierto')
      .attr('aria-hidden', 'false');
  });

  $('#cerrarModal,#modalOferta').on('click', function(e) {
    if (e.target.id === 'cerrarModal' || e.target.id === 'modalOferta') {
      $('#modalOferta')
        .fadeOut(200)
        .removeClass('abierto')
        .attr('aria-hidden', 'true');
    }
  });

  $('.tarjeta').hide().fadeIn(700);
});
