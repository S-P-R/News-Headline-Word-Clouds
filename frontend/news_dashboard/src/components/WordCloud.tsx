import '../styles/WordCloud.css'
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import cloud from 'd3-cloud';


const MAX_CLOUD_SIZE = 1250

const WordCloud = ({ words }) => {
  const svgRef = useRef();

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

  const randomColor = () => {
    let colors = ["#434343", "#6e6e6e", "#8A8A8A"]
    return colors[Math.floor(Math.random() * colors.length)];
  }; /* TODO: remove? */

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove(); /* Clean up previous word cloud renders */
    
    const dim = Math.min(window.innerWidth, window.innerHeight, MAX_CLOUD_SIZE)
    const width = dim;
    const height = dim;
    console.log("DIM: ", dim)
    svg.attr('width', width).attr('height', height);

    let word_counts = words.map((w) => w[1])
    let min_count = word_counts.reduce((a, b) => Math.min(a, b), word_counts[0])
    let max_count = word_counts.reduce((a, b) => Math.max(a, b), word_counts[0])
  
    // const root = document.documentElement
    // let scale = Number(window.getComputedStyle(root).getPropertyValue("font-size").slice(0, -2))
    // scale = scale * 28
    // console.log("SCALE: ", scale)

    let scaled_words = words.map(w => ([w[0], normalize(w[1], min_count, max_count, 1, dim)]))  
    scaled_words = scaled_words.map(w => ([w[0], logistic(w[1], 50, .05, 45)]))  

    const layout = cloud()
      .words(scaled_words.map(d => ({ text: d[0], size:d[1]})))
      .spiral("rectangular")
      .size([width, height])
      .padding(5)
      .rotate(() => (~~(Math.random() * 6) - 3) * 30)
      .font('Times New Roman')
      .fontSize(d => d.size)
      .on('end', draw);

    layout.start();

    function draw(words) {
      const group = svg
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`)
      .selectAll('text')
      .data(words)
      .enter()
      .append('text')
      .style('font-size', d => `${d.size}px`)
      .style('font-weight', `700`)
      .style('fill', function(d) { return randomColor(); })
      .attr('text-anchor', 'middle')
      .attr('transform', d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
      .style('opacity', 0) 
      // .style('overflow', `visible`)
      .text(d => d.text)

      group /* Makes words fade-in */
      .transition()
      .duration(800)
      .style('opacity', 1)
    }
      // return () => {
      //   svg.selectAll('*').remove(); /* Clean up previous word cloud renders */
      // };
      // svg.selectAll('*').remove(); /* Clean up previous word cloud renders */


    // return () => window.removeEventListener('resize', handleResize);
    // return () => {
    //   svg.selectAll('*').remove(); /* Clean up previous word cloud renders */
    // };
  }, [words]);


  return <div className="word-cloud-wrapper"> <svg className="word-cloud" ref={svgRef}></svg> </div>;
};

export default WordCloud;