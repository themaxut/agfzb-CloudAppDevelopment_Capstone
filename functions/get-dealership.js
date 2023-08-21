const express = require("express");

const app = express();
const port = 3000;
const Cloudant = require("@cloudant/cloudant");

// Initialize Cloudant connection
function dbCloudantConnect() {
    return new Promise((resolve, reject) => {
        Cloudant(
            {
                // eslint-disable-line
                url: "https://1f8ba730-6274-498e-bdc8-06a9d13ea97d-bluemix.cloudantnosqldb.appdomain.cloud", //Enter your Cloudant service URL here
            },
            (err, cloudant) => {
                if (err) {
                    console.error(
                        "Connect failure: " + err.message + " for Cloudant DB"
                    );
                    reject(err);
                } else {
                    let db = cloudant.use("dealerships");
                    console.info("Connect success! Connected to DB");
                    resolve(db);
                }
            }
        );
    });
}

let db;

dbCloudantConnect()
    .then((database) => {
        db = database;
    })
    .catch((err) => {
        throw err;
    });

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
app.get("/dealerships/get", (req, res) => {
    const { state, id } = req.query;
});
