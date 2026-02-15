CKEDITOR.editorConfig = function(config) {
    config.removePlugins = 'exportpdf,scayt,wsc';
    config.filebrowserUploadUrl = '/ckeditor/upload/';
    config.filebrowserBrowseUrl = '/ckeditor/browse/';
    config.allowedContent = true;
};