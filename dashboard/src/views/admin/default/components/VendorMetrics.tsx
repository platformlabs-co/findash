import Card from "components/card";
import ComplexTable from "./ComplexTable";
import tableDataComplex from "./../variables/tableDataComplex"
import { useAuth0 } from "@auth0/auth0-react";

const VendorMetrics = (props: { vendorName: String }) => {
  const {  getAccessTokenSilently } = useAuth0();
  const token =  getAccessTokenSilently();
  
  // Make an HTTP request to the server and send the token in the Authorization header
  const server_url = "http://localhost:8000/v1/vendors-metrics"
  const data = fetch(server_url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return (
    <Card extra="pb-10 p-[20px]">
      <h1 className="uppercase text-cemter font-bold title">{props.vendorName}</h1>
      <ComplexTable tableData={tableDataComplex}/> 
    </Card>
  );
};

export default VendorMetrics;
