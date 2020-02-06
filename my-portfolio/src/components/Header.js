import React, { Component } from 'react'

export default class Header extends Component {
  render() {
    return (
      <div>
        <h1 className="color--skyBlue section__heading--largest">
        Tausif Solaiman
      </h1>

      <ul className="section--social">

        {/* <!--Links to relevant professional social media & resume -->
        <!-- See: http://fontawesome.io/icons/#brand for more -->

        <!-- Link to Linked In profile --> */}
        <li className="socialWrapper">
          <a className="color--skyBlue social"
             title="LinkedIn Profile"
             href="https://linkedin.com/in/tausif-solaiman">
            <i className="fa fa-linkedin"></i>
          </a>
        </li>
{/* 
        <!-- Link to GitHub profile --> */}
        <li className="socialWrapper color--skyBlue">
          <a className="social color--skyBlue"
             title="GitHub Profile" 
             href="https://github.com/TauSolaiman">
            <i className="fa fa-github"></i>
          </a>
        </li>

        {/* <!-- Link to resume, probably a .pdf --> */}
        <li className="socialWrapper">
          <a className="social color--skyBlue"
             title="Resume"
             href="Tausif Solaiman Resume.pdf">
            <i className="fa fa-file-text"></i>
          </a>
        </li>
      </ul>
      </div>
    )
  }
}

