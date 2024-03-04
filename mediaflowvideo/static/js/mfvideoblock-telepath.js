// js/import-text-block.js

class MountVideoDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        
        /*
        Not really needed anymore?

        document.getElementById(prefix + '-mf-media_id').value = initialState.media_id;
        document.getElementById(prefix + '-mf-file_id').value = initialState.selected_file;
        document.getElementById(prefix + '-mf-autoplay').value = initialState.autoplay ? '1"' : '0';
        document.getElementById(prefix + '-mf-embed_method').value = initialState.embed_method;
        document.getElementById(prefix + '-mf-start_offset').value = initialState.start_offset;        
        
        */
       
        return block;
    }
}

window.telepath.register('mediaflowvideo.MfVideoBlock', MountVideoDefinition);
console.info('telepath path registered for MfVideoBlock')
