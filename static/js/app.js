const productos = JSON.parse(document.getElementById('productos-data').textContent);
const ofertas = JSON.parse(document.getElementById('ofertas-data').textContent);
const noticias = JSON.parse(document.getElementById('noticias-data').textContent);

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
const sinNoticias = document.getElementById('mensajeSinNoticias');

sinNoticias.classList.toggle('oculto', noticias.length > 0);
noticias.forEach(n => {
  const a = document.createElement('article');
  a.className = 'noticia-card';
  a.innerHTML = `
    <img src="${n.imagen}" alt="${n.titulo}">
    <div class="noticia-contenido">
      <small>${n.fecha}</small>
      <h3>${n.titulo}</h3>
      <p>${n.contenido}</p>
    </div>`;
  noticiasCont.appendChild(a);
});

const ofertasCont = document.getElementById('contenedorOfertas');
const sinOfertas = document.getElementById('mensajeSinOfertas');

sinOfertas.classList.toggle('oculto', ofertas.length > 0);
ofertas.forEach(oferta => {
  const article = document.createElement('article');
  article.className = 'oferta-card';
  article.innerHTML = `
    <img src="${oferta.imagen}" alt="${oferta.producto}">
    <div class="oferta-contenido">
      <span class="categoria">${oferta.categoria}</span>
      <h3>${oferta.producto}</h3>
      <p>${oferta.descripcion}</p>
      <p class="precio"><del>$${oferta.precio_anterior.toFixed(2)}</del> <strong>$${oferta.precio_oferta.toFixed(2)}</strong></p>
      <button class="boton ver-oferta" data-id="${oferta.id}">Ver detalles</button>
    </div>`;
  ofertasCont.appendChild(article);
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

  $('.ver-oferta').on('click', function() {
    const oferta = ofertas.find(item => item.id === Number($(this).data('id')));
    if (oferta) {
      $('#modalOfertaTitulo').text(oferta.producto);
      $('#modalOfertaTexto').text(oferta.descripcion);
    }

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
