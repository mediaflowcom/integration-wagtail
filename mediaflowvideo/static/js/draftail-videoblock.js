
class VideoSource extends window.React.Component {
  componentDidMount() {
    console.log('component mounted');    
    ModalWorkflow({                    
        url: '/admin/mfvideomodal/?trigger=' + 'draftail'
    });
    console.log('mounted');
    const { editorState, entityType, onComplete } = this.props;

    console.log('continuing');
    
    
    // Uses the Draft.js API to create a new entity with the right data.
   

    var listener = window.addEventListener('mf-video-selected', (e)=>  {
        const content = editorState.getCurrentContent();
        const selection = editorState.getSelection();    
        const contentWithEntity = content.createEntity(
            entityType.type,
            'IMMUTABLE',
            e.detail
            );
            const entityKey = contentWithEntity.getLastCreatedEntityKey();
        
            // We also add some text for the entity to be activated on.
            const text = `MEDIAFLOWVIDEO`;
        
            const newContent = window.DraftJS.Modifier.replaceText(
                content,
                selection,
                text,
                null,
                entityKey,
            );
            const nextState = window.DraftJS.EditorState.push(
                editorState,
                newContent,
                'insert-characters',
            );
            onComplete(nextState);
    });
    onComplete(editorState);
    
  }

  render() {
    return null;
  }
}

const Video = (props) => {
    const { entityKey, contentState } = props;
    const data = contentState.getEntity(entityKey).getData();    
      
    return window.React.createElement(
      'iframe',
      {
        style: {width:'320px', height:'200px'},
        src: `https://play.mediaflowpro.com/ovp/11/${data.mediaId}`,       
      },
      props.children,
    );
  };

  // Register the plugin directly on script execution so the editor loads it when initialising.
window.draftail.registerPlugin({
  type: 'MF_VIDEO',
  source: VideoSource,
  decorator: Video,
}, 'entityTypes');
