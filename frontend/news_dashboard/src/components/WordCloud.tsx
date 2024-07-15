import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import cloud from 'd3-cloud';


function logistic(x: number, max: number = 1, growth_rate: number = 1, x_midpoint: number = 0): number {
  return max / (1 + Math.exp(-growth_rate * (x - x_midpoint)));
}

function normalize(value: number, curr_range_min: number, curr_range_max: number, 
                   desired_min: number, desired_max: number): number {
  /* Scales value between 0 and 1 */
  let scaled = (value - curr_range_min)  / (curr_range_max - curr_range_min)   
  /* Scaled values into desired range */
  scaled = scaled * (desired_max - desired_min) + desired_min
  return scaled
}

const WordCloud = ({ words }) => {
  const svgRef = useRef();
  const randomColor = () => {
    let colors = ["#434343", "#6e6e6e", "#8A8A8A"]
    return colors[Math.floor(Math.random() * colors.length)];
  }; /* TODO: remove? */


  useEffect(() => {
    const svg = d3.select(svgRef.current);
    // const width = 800;
    // const height = 800;
    const width = 750;
    const height = 750;

    svg.attr('width', width).attr('height', height);

    let word_counts = words.map((w) => w[1])
    let min_count = word_counts.reduce((a, b) => Math.min(a, b), word_counts[0])
    let max_count = word_counts.reduce((a, b) => Math.max(a, b), word_counts[0])

  
   
    let scaled_words = words.map(w => ([w[0], normalize(w[1], min_count, max_count, 1, 500)]))  
    scaled_words = scaled_words.map(w => ([w[0], logistic(w[1], 50, .05, 45)]))  

    const layout = cloud()
      .spiral("rectangular")
      .size([width, height])
      .words(scaled_words.map(d => ({ text: d[0], size:d[1]})))
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
        .style('fill', function(d) { return randomColor(); })
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