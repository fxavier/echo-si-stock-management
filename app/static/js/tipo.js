var Sigc = Sigc || {};

Sigc.ComboTipoEmitente = (function () {
   

    function ComboTipoEmitente() {
        this.combo = $('#id_tipo_emitentes');
        this.emitter = $({});
        this.on = this.emitter.on.bind(this.emitter);
    }

    ComboTipoEmitente.prototype.iniciar = function () {
        this.combo.on('change', onTipoEmitenteAlterado.bind(this));
    }

    function onTipoEmitenteAlterado() {
        console.log('Tipo emitente:', this.combo.val());
    }
    
    return ComboTipoEmitente;
}());

$(function() {
   var comboTipoEmitente = new Sigc.ComboTipoEmitente();
   comboTipoEmitente.iniciar();
});