import React from "react";
import { useState, useEffect, useRef } from "react";
import "./styles.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/sb-admin-2.css";
import NetworkGraph from "./components/ngraph";
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Modal,
  InputGroup,
  FormControl
} from "react-bootstrap";
import { panels, panelsBody } from "./panel/panels";
import { hardcopy } from "./util/util";
import Request from "axios-request-handler";
import Switch from "./components/switch";
import HijackingTable from "./components/table";
import { set } from "d3";
import IpContext from "./context/IPcontext";
import DegreeContext from "./context/DegreeContext";
import WithdrawnContext from "./context/WithdrawnContext";
import MEDContext from "./context/MEDContext";
import AsPathContext from "./context/aspath";

import { httpaddr } from "./net/net";

export default function App() {
  const [ipdata, setipdata] = useState(
    "AS,frequency\n3759,0.9999\n4578,0.0001"
  );
  const [degreeData, setDegreeData] = useState(
    "date,close\n1,93.24\n2,95.35\n3,98.84\n40000000,99.92"
  );
  const [withdrawnData, setwithdrawnData] = useState(
    "date,close\n1,93.24\n2,95.35\n3,98.84\n40000000,99.92"
  );

  const [MED, setMED] = useState(
    "date,close\n1,93.24\n2,95.35\n3,98.84\n40000000,99.92"
  );

  const [AsPath, setAsPath] = useState(
    "date,close\n1,93.24\n2,95.35\n3,98.84\n40000000,99.92"
  );
  const [ipbar, setipbar] = useState("AS,frequency\n3759,0.9999\n4578,0.0001");
  const [ipad, setipad] = useState("179.189.84.0/23");
  const ipAddress = useRef(null);
  const asNumber = useRef(null);
  const [show, setShow] = useState(false);
  const [showpPanelController, setshowpPanelController] = useState(false);
  const [AllPanels, setAllPanels] = useState(panels);
  const [showpAlertController, setshowpAlertController] = useState(false);
  const [showIPAddressController, setshowIPAddressController] = useState(false);
  const [ndata, setndata] = useState(12);
  const [nattackerNodeID, setnattackerNodeID] = useState(-1);
  const handleGraphData = (vertex) => {
    //const graph = new Request("http://127.0.0.1:5000/graph", {});
  };
  const changeIP = () => {
    setipdata(
      "letter,frequency\nA,0.08167\nB,0.01492\nC,0.02782\nD,0.04253\nE,0.12702"
    );
  };
  const fetchDegree = () => {
    const degreedist = new Request(httpaddr + "degreedist");
    degreedist.get().then((res) => {
      setDegreeData(res.data);
    });
  };
  const fetchWithdrawn = () => {
    const degreedist = new Request(httpaddr + "withdrawndist");
    degreedist.get().then((res) => {
      setwithdrawnData(res.data);
    });
  };

  const fetchMED = () => {
    const degreedist = new Request(httpaddr + "aggregatemulti");

    degreedist.get().then((res) => {
      setMED(res.data);
    });
  };

  const fetchASpath = () => {
    const degreedist = new Request(httpaddr + "aspathlength");

    degreedist.get().then((res) => {
      setAsPath(res.data);
    });
  };

  useEffect(() => {
    handleGraphData(null);
    // const rI = new Request("http://127.0.0.1:5000/detect");
    // const fetchData = () => {
    //   rI.poll(500).get((response) => {
    //     //callback function that executes in every response
    //     //if return false the interval will discontinue
    //     setTimex(response.data);
    //   });
    // };
    // fetchData();
    fetchMED();
    fetchDegree();
    fetchWithdrawn();
    fetchASpath();
  }, [ndata]);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleClosePanelController = () => setshowpPanelController(false);
  const handleShowPanelController = () => setshowpPanelController(true);
  const handleCloseAlertController = () => setshowpAlertController(false);
  const handleShowAlertController = () => setshowpAlertController(true);
  const handleCloseIPAddressController = () =>
    setshowIPAddressController(false);
  const handleShowIPAddressController = () => setshowIPAddressController(true);
  const changeShowPanel = (title) => {
    var copy = hardcopy(AllPanels);
    for (var i = 0; i < copy.length; ++i)
      if (copy[i].title === title) copy[i].show = !copy[i].show;
    setAllPanels(copy);
  };
  const buttonChange = (title) => {
    return () => {
      changeShowPanel(title);
    };
  };
  const setipxx = (ip) => {
    const degreedist = new Request(httpaddr + "getASbasedonip?ip=" + ip);

    degreedist.get().then((res) => {
      setipbar(res.data);
    });
  };
  const handleIPAddress = () => {
    console.log(ipAddress.current.value);
    setipxx(ipAddress.current.value);
    handleCloseIPAddressController();
  };
  const FindAS = () => {
    console.log(asNumber.current.value);
    setndata(asNumber.current.value);
    handleClose();
  };

  const getnext100AS = () => {
    setndata(ndata + 100);
  };
  const getprevious100AS = () => {
    if (ndata - 100 > 0) setndata(ndata - 100);
    else setndata(1);
  };

  const setattackerAS = (victim, attacker, ips) => {
    setndata(parseInt(victim, 10));
    setnattackerNodeID(parseInt(attacker, 10));
    setipxx(ips);
  };

  const showallpanelsfromsettings = () => {
    var ret = [];
    var rows = [];
    var cols = [];
    var n = AllPanels.length;
    for (var i = 0; i < n; ++i)
      if (AllPanels[i].show)
        cols.push(
          <Col xl={4} lg={4}>
            <Card>
              <Card.Header>{AllPanels[i].title}</Card.Header>
              <Card.Body>{panelsBody[i].body /*AllPanels[i].body*/}</Card.Body>
            </Card>
          </Col>
        );
    var i = 0;
    while (i + 3 < n) {
      rows.push(
        <Row>
          {cols[i]} {cols[i + 1]} {cols[i + 2]}
        </Row>
      );
      i = i + 3;
    }
    if (i < n) {
      rows.push(
        <Row>
          {i < n ? cols[i] : ""} {i + 1 < n ? cols[i + 1] : ""}{" "}
          {i + 2 < n ? cols[i + 2] : ""}
        </Row>
      );
    }

    return rows;
  };

  const PanelControllerButtons = () => {
    var ret = [];
    var n = AllPanels.length;
    for (var i = 0; i < n; ++i) {
      ret.push(
        <div>
          <span>
            {AllPanels[i].title} :
            <Switch
              id={i}
              isOn={AllPanels[i].show}
              handleToggle={buttonChange(AllPanels[i].title)}
            ></Switch>
          </span>
        </div>
      );
    }
    return ret;
  };

  return (
    <div className="App">
      <IpContext.Provider value={ipbar}>
        <AsPathContext.Provider value={AsPath}>
          <MEDContext.Provider value={MED}>
            <WithdrawnContext.Provider value={withdrawnData}>
              <DegreeContext.Provider value={degreeData}>
                <Container>
                  <Row>
                    <Col xl={8} lg={7}>
                      <Card>
                        <Card.Header>
                          BGP AS connection visualization
                        </Card.Header>
                        <Card.Body>
                          <NetworkGraph
                            nodeid={ndata}
                            attackerNodeID={nattackerNodeID}
                          ></NetworkGraph>
                          {/* BGP router connection visualization*/}
                        </Card.Body>
                      </Card>
                    </Col>
                    <Col xl={4} lg={5}>
                      <Card>
                        <Card.Header>Action Panel</Card.Header>
                        <Card.Body>
                          <p>
                            <Button variant="primary" onClick={getnext100AS}>
                              Go to next 100 AS
                            </Button>
                          </p>
                          <p>
                            <Button
                              variant="primary"
                              onClick={getprevious100AS}
                            >
                              Go to previous 100 AS
                            </Button>
                          </p>
                          <p>
                            <Button variant="primary" onClick={handleShow}>
                              Locate specific AS
                            </Button>
                          </p>
                          <p>
                            <Button
                              variant="warning"
                              onClick={handleShowAlertController}
                            >
                              Check all the alerts
                            </Button>
                          </p>
                          <p>
                            <Button
                              variant="primary"
                              onClick={handleShowPanelController}
                            >
                              Add more panels
                            </Button>
                          </p>
                          <p>
                            <Button
                              variant="primary"
                              onClick={handleShowIPAddressController}
                            >
                              Locate Specific IP
                            </Button>
                          </p>

                          {/*Action Panel*/}
                        </Card.Body>
                      </Card>
                    </Col>
                  </Row>
                  {showallpanelsfromsettings()}
                </Container>

                <Modal show={show} onHide={handleClose}>
                  <Modal.Header closeButton>
                    <Modal.Title>Please Enter As Number</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>
                    <InputGroup>
                      <InputGroup.Prepend>
                        <InputGroup.Text id="inputGroup-sizing-sm">
                          As Number
                        </InputGroup.Text>
                      </InputGroup.Prepend>
                      <FormControl
                        ref={asNumber}
                        aria-label="Small"
                        aria-describedby="inputGroup-sizing-sm"
                      />
                    </InputGroup>
                  </Modal.Body>
                  <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                      Close
                    </Button>
                    <Button variant="primary" onClick={FindAS}>
                      Go
                    </Button>
                  </Modal.Footer>
                </Modal>
                <Modal
                  show={showpPanelController}
                  onHide={handleClosePanelController}
                >
                  <Modal.Header closeButton>
                    <Modal.Title>
                      Please Choose the options for the panels
                    </Modal.Title>
                  </Modal.Header>
                  <Modal.Body>{PanelControllerButtons()}</Modal.Body>
                  <Modal.Footer>
                    <Button
                      variant="secondary"
                      onClick={handleClosePanelController}
                    >
                      Close
                    </Button>
                  </Modal.Footer>
                </Modal>
                <Modal
                  show={showpAlertController}
                  onHide={handleCloseAlertController}
                  size="lg"
                >
                  <Modal.Header closeButton>
                    <Modal.Title>
                      Please choose an action to take for a specific alert
                    </Modal.Title>
                  </Modal.Header>
                  <Modal.Body>
                    <HijackingTable saa={setattackerAS}></HijackingTable>
                  </Modal.Body>
                  <Modal.Footer>
                    <Button
                      variant="secondary"
                      onClick={handleCloseAlertController}
                    >
                      Close
                    </Button>
                  </Modal.Footer>
                </Modal>

                <Modal
                  show={showIPAddressController}
                  onHide={handleCloseIPAddressController}
                >
                  <Modal.Header closeButton>
                    <Modal.Title>
                      Please choose a specific IP address to inspect
                    </Modal.Title>
                  </Modal.Header>
                  <Modal.Body>
                    <InputGroup>
                      <InputGroup.Prepend>
                        <InputGroup.Text id="ip_address_bar">
                          IP Address
                        </InputGroup.Text>
                      </InputGroup.Prepend>
                      <FormControl
                        ref={ipAddress}
                        id="ip_address_controller"
                        aria-label="Small"
                        aria-describedby=""
                      />
                    </InputGroup>
                  </Modal.Body>
                  <Modal.Footer>
                    <Button
                      variant="secondary"
                      onClick={handleCloseIPAddressController}
                    >
                      Close
                    </Button>
                    <Button variant="primary" onClick={handleIPAddress}>
                      Go
                    </Button>
                  </Modal.Footer>
                </Modal>
              </DegreeContext.Provider>
            </WithdrawnContext.Provider>
          </MEDContext.Provider>
        </AsPathContext.Provider>
      </IpContext.Provider>
    </div>
  );
}
