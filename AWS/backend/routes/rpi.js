const router = express().Router();
router.get("/", (req, res) => {
  console.log("hi");
});
module.exports = router;
