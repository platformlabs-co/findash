import React from "react";
import Chart from "react-apexcharts";

type ChartProps = {
  // using `interface` is also ok
  [x: string]: any;
};
type ChartState = {
  chartData: any[];
  chartOptions: any;
};

class ColumnChart extends React.Component<ChartProps, ChartState> {
  constructor(props: { chartData: any[]; chartOptions: any }) {
    super(props);
    this.state = {
      chartData: props.chartData || [],
      chartOptions: props.chartOptions || {},
    };
  }

  componentDidMount() {
    this.setState({
      chartData: this.props.chartData || [],
      chartOptions: this.props.chartOptions || {},
    });
  }

  componentDidUpdate(prevProps: ChartProps) {
    if (prevProps.chartData !== this.props.chartData || prevProps.chartOptions !== this.props.chartOptions) {
      this.setState({
        chartData: this.props.chartData || [],
        chartOptions: this.props.chartOptions || {},
      });
    }
  }

  render() {
    if (!this.state.chartData || !Array.isArray(this.state.chartData)) {
      return <div>Loading...</div>;
    }

    return (
      <Chart
        options={this.state.chartOptions}
        series={this.state.chartData}
        type="bar"
        width="100%"
        height="100%"
      />
    );
  }
}

export default ColumnChart;
