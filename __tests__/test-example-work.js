import React from 'react';
import { shallow } from 'enzyme';
import ExampleWork, { ExampleWorkBubble } from '../js/example-work';

import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
Enzyme.configure({ adapter: new Adapter() });

const myWork = [
  {
    'title': "PRODUCTS",
    'image': {
      'desc': "example screenshot of a project involving code",
      'src': "images/example1.png",
      'comment': ""
    }
  },
  {
    'title': "SOLUTIONS",
    'image': {
      'desc': "example screenshot of a project involving chemistry",
      'src': "images/example2.png",
      'comment': ""
    }
  }
];

describe("ExampleWork component", () => {

    let component = shallow(<ExampleWork work={myWork}/>);

    it("Should be a 'section' element", () => {
      console.log(component.debug());
      expect(component.type()).toEqual('section');
    });

    it("Should contain as many children as there are work examples", () => {
      expect(component.find("ExampleWorkBubble").length).toEqual(myWork.length);
    });
});
