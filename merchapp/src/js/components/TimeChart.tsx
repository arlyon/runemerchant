import React from "react";
import Chart from "chart.js"

interface ITimeChartProps {
    name: string,
    data: {
        t: Date,
        y: number,
    }[]
}

export class TimeChart extends React.Component<ITimeChartProps, {}> {

    private graph: HTMLCanvasElement | null = null;

    componentDidMount(): void {
        const context = this.graph!.getContext('2d');
        new Chart(context!, {
            type: 'line',
            data: {
                datasets: [{
                    label: this.props.name,
                    data: this.props.data,
                    fill: false,
                    backgroundColor: 'hsl(220, 69%, 49%)',
                    borderColor: 'hsl(220, 69%, 49%)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            round: "minute",
                            minUnit: "day"
                        }
                    }]
                }
            }
        });
    }

    render(): React.ReactNode {
        return <canvas ref={(node) => this.graph = node} height="300"/>
    }

}