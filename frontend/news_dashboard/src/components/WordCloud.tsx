import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import cloud from 'd3-cloud';


function logistic(x: number, max: number = 1, growth_rate: number = 1, x_midpoint: number = 0): number {
  return max / (1 + Math.exp(-growth_rate * (x - x_midpoint)));
}

const WordCloud = ({ words }) => {
  const svgRef = useRef();

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 800;

    svg.attr('width', width).attr('height', height);

    const layout = cloud()
      .size([width, height])
      .words(words.map(d => ({ text: d[0], size: logistic(d[1], 50, .05, 45) })))
      .padding(5)
      .rotate(() => (~~(Math.random() * 6) - 3) * 30)
      .font('Impact')
      .fontSize(d => d.size)
      .on('end', draw);

    layout.start();

    function draw(words) {
      svg
        .append('g') 
        .attr('transform', `translate(${width / 2},${height / 2})`)
        .selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .style('font-size', d => `${d.size}px`)
        .style('font-family', 'Impact')
        .style('fill', (d, i) => 'grey')
        .attr('text-anchor', 'middle')
        .attr('transform', d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
        .text(d => d.text);
    }

    return () => {
      svg.selectAll('*').remove(); /* Clean up previous word cloud renders */
    };
  }, [words]);

  return <svg ref={svgRef}></svg>;
};


// const WordCloud = ({ words }) => {
//   const svgRef = useRef();

//   useEffect(() => {
//     const svg = d3.select(svgRef.current);
//     const width = 500;
//     const height = 500;

//     svg.attr('width', width).attr('height', height);

//     const layout = cloud()
//       .size([width, height])
//       .words(words.map(d => ({ text: d, size: 10 + Math.random() * 90 })))
//       .padding(5)
//       .rotate(() => (~~(Math.random() * 6) - 3) * 30)
//       .font('Impact')
//       .fontSize(d => d.size)
//       .on('end', draw);

//     layout.start();

//     function draw(words) {
//       svg
//         .append('g') 
//         .attr('transform', `translate(${width / 2},${height / 2})`)
//         .selectAll('text')
//         .data(words)
//         .enter()
//         .append('text')
//         .style('font-size', d => `${d.size}px`)
//         .style('font-family', 'Impact')
//         .style('fill', (d, i) => 'grey')
//         .attr('text-anchor', 'middle')
//         .attr('transform', d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
//         .text(d => d.text);
//     }

//     return () => {
//       svg.selectAll('*').remove(); /* Clean up previous word cloud renders */
//     };
//   }, [words]);

//   return <svg ref={svgRef}></svg>;
// };

export default WordCloud;