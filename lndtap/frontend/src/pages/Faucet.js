import React, { Component } from 'react';
import { Jumbotron, Form, FormGroup, Input, Label, Button, Progress } from 'reactstrap';

import Api from '../common/Api';

const styles = {
  formContainer: {
    padding: 20,
    border: '1px solid #d8d8d8'
  }
}

export default class Faucet extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
      error: null,
      form: {},
      channelInfo: {}
    };

    this.onChange = this.onChange.bind(this);
    this.createChannel = this.createChannel.bind(this);
  }

  componentWillMount() {
    //this.fetchStats();
  }

  onChange(elem, value) {
    console.log('Updating state to ', { ...this.state.form, [elem]: value });
    this.setState({
      form: { ...this.state.form, [elem]: value }
    });
  }


  createChannel() {
    this.setState({ isLoading: true });
    Api.createChannel(this.state.form)
    .then(response =>
      this.setState({
        channelInfo: response
      })
    )
    .catch(error => {
      this.setState({ error });
    })
    .finally(() => {
      this.setState({ isLoading: false });
    });
  }

  render() {
    return (
      <div>
        <Jumbotron style={{ padding: 20 }}>
          <h1>LndTap</h1>
          <p className="lead">Faucet for Bitcoin Tesnet on Lightening Network</p>
          <hr className="my-2" />
          <p>Peer Address</p>
          <p className="lead">
            03193d512b010997885b232ecd6b300917e5288de8785d6d9f619a8952728c78e8
          </p>
        </Jumbotron>
        {this.state.isLoading && (
          <Progress striped color="primary" value="100">
            {" "}
            Creating Channel{" "}
          </Progress>
        )}
        <div style={styles.formContainer}>
          <p className="text-center"> Enter following details to create a new channel with the faucet and get some initial balance </p>
          <Form>
            <FormGroup>
              <Label for="host">Host</Label>
              <Input type="text" name="host" id="host" placeholder="Enter IP Address" onChange={e => this.onChange('host', e.target.value)} />
            </FormGroup>
            <FormGroup>
              <Label for="publicKey">Public Identifier</Label>
              <Input type="text" name="publicKey" id="publicKey" placeholder="Enter Target Node Public Key" onChange={e => this.onChange('pubkey', e.target.value)}/>
            </FormGroup>
            <FormGroup>
              <Label for="channelAmount">Channel Amount (in Satoshis)</Label>
              <Input type="number" name="channelAmount" id="channelAmount" placeholder="Max is 16 million" onChange={e => this.onChange('channel_amount', parseInt(e.target.value))} />
            </FormGroup>
            <FormGroup>
              <Label for="initialBalance">Initial Balance (in Satoshis)</Label>
              <Input type="number" name="initialBalance" id="initialBalance" placeholder="Total amount to be sent initially" onChange={e => this.onChange('initial_balance', parseInt(e.target.value))}/>
            </FormGroup>
            <Button color="primary" className="text-center" onClick={this.createChannel}>Submit</Button>
          </Form>
        </div>
      </div>
    );
  }



}