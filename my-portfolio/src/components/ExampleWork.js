import React, { Component } from 'react'

const myWork = [
  {
    'title': "Squeezy: SQL Made Easy",
    'image': {
      'desc': "A SQL Query Chatbot",
      'src': "/images/squeezy_graph.png",
    }
  },
  {
    'title': "Binance Trading Models",
    'image': {
      'desc': "Algorithmic trading stradegies for Binance Exchange graphed with plotly",
      'src': "/images/StrategyEval.png",
    }
  },
  {
    'title': "",
    'image': {
      'desc': "",
      'src': "",
    }
  },
]

export default class ExampleWork extends Component {
  render() {
    return (
      <section className="section section--alignCentered section--description">

      {myWork.map(((example) => {
            return (
              <div className="section__exampleWrapper">
                <div className="section__example">
                  <img alt={example.desc}
                       className="image_class"
                       src={example.image.src}
                       />
                  <dl className="color--cloud">
                    <dt className="section__exampleTitle section__text--centered">
                      {example.title}
                    </dt>
                    <dd></dd>
                  </dl>
                </div>
              </div>
            )
      }))}
    </section>
    )
  }
}




