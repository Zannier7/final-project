import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import AutosList from '../AutosList';

const autos = [
    {
        'color':'blanco',
        'id':1,
        'marca':'bmw',
        'modelo':'ci3',
        'placa':'7u456a',
        'tipo':'deportivo'
    },
    {
        'color':'negro',
        'id':2,
        'marca':'audio',
        'modelo':'uik',
        'placa':'5625as',
        'tipo':'4x4'
    },
    {
        'color':'negro-gris',
        'id':3,
        'marca':'volvo',
        'modelo':'mc7',
        'placa':'45as15',
        'tipo':'suv'
    }
];

test('AutosList renders properly', () => {
  const wrapper = shallow(<AutosList autos={autos}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(3);
  expect(element.get(0).props.children).toBe('bmw');
});

test('AutosList renders a snapshot properly', () => {
  const tree = renderer.create(<AutosList autos={autos}/>).toJSON();
  expect(tree).toMatchSnapshot();
});
