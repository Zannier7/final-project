import React from 'react';

const AutosList = (props) => {
  return (
    <div>
      {
        props.autos.map((autos) => {
          return (
            <h4
              key={autos.id}
              className="box title is-4"
            >{ autos.marca }
            </h4>
          )
        })
      }
    </div>
  )
};

export default AutosList;
